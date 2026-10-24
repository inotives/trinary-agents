import ast
import contextlib
import importlib.util
import io
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
SCRIPT = SKILL / "scripts" / "render_report.py"
REPORT_TEMPLATE = (SKILL / "references" / "report-template.md").read_text(encoding="utf-8")
PLAN_TEMPLATE = (SKILL / "references" / "plan-template.md").read_text(encoding="utf-8")
sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location("render_report", SCRIPT)
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)

REPORT_KEYS = ("id", "title", "status", "branch", "plan_approved_at", "reported_at", "review", "reviewer")
REPORT_SECTIONS = (
    "Outcome", "Acceptance checks", "Changes", "Findings", "Review", "Pending issues", "Steps completed",
)
NAMESPACE_URIS = {"http://www.w3.org/2000/svg", "http://www.w3.org/1999/xlink"}


def make_folder(temp, report=REPORT_TEMPLATE, plan=PLAN_TEMPLATE, project_line="Project name: Example Project"):
    workspace = Path(temp) / "trinary-workspace"
    folder = workspace / "rapid" / "RF-0001--example-rapid-feature"
    folder.mkdir(parents=True)
    if project_line is not None:
        (workspace / "README.md").write_text(f"# Trinary workspace\n\n{project_line}\n", encoding="utf-8")
    if report is not None:
        (folder / "report.md").write_text(report, encoding="utf-8")
    if plan is not None:
        (folder / "README.md").write_text(plan, encoding="utf-8")
    return folder


def run(folder):
    """Call main() in-process; return (exit code, stdout, stderr)."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = renderer.main([str(folder)])
    return code, out.getvalue(), err.getvalue()


def drop_section(text, heading):
    """Remove a `## heading` and its body up to the next `##` heading."""
    return re.sub(rf"^## {re.escape(heading)}\n.*?(?=^## |\Z)", "", text, flags=re.S | re.M)


def set_key(text, key, value):
    return re.sub(rf"^{key}:.*$", f"{key}: {value}", text, count=1, flags=re.M)


class ValidReportTests(unittest.TestCase):
    def render_template(self, report=REPORT_TEMPLATE, plan=PLAN_TEMPLATE):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        folder = make_folder(temp.name, report=report, plan=plan)
        code, out, err = run(folder)
        self.assertEqual(code, 0, err)
        return (folder / "report.html").read_text(encoding="utf-8")

    def test_committed_templates_render(self):
        page = self.render_template()
        self.assertTrue(page.startswith("<!doctype html>\n" + renderer.MARKER))
        self.assertIn(
            "<title>Trinary-RAPID Report :: Example Project :: RF-0001 Example rapid feature</title>", page
        )

    def test_page_embeds_stylesheet_license_and_marker(self):
        page = self.render_template()
        self.assertIn('<style id="daisyui-styles">', page)
        self.assertIn("/*! 🌼 daisyUI 5.7.50 - MIT License */", page)
        self.assertIn("DaisyUI 5.7.50 — MIT", page)
        self.assertIn("Copyright (c) 2020 Pouya Saadeghi", page)
        self.assertIn("Permission is hereby granted, free of charge", page)
        self.assertIn(renderer.MARKER, page)

    def test_page_embeds_report_theme_with_both_palettes(self):
        page = self.render_template()
        match = re.search(r'<style id="report-theme">(.*?)</style>', page, re.S)
        self.assertIsNotNone(match)
        theme = match.group(1)
        self.assertIn(':root[data-theme="dark"]', theme)
        self.assertIn(':root[data-theme="light"]', theme)
        self.assertLess(page.index('id="daisyui-styles"'), page.index('id="report-theme"'))
        self.assertIn('<html lang="en" data-theme="dark">', page)

    def test_page_has_theme_toggle_button(self):
        page = self.render_template()
        self.assertIn('<button id="theme-toggle"', page)
        self.assertIn('type="button"', page)
        script = re.search(r"<script>(.*?)</script>", page, re.S).group(1)
        self.assertIn('getElementById("theme-toggle")', script)
        self.assertIn(renderer.THEME_STORAGE_KEY, script)
        self.assertIn("localStorage", script)
        self.assertNotIn("</", script)

    def test_result_badge_and_every_section(self):
        page = self.render_template()
        self.assertIn('id="result-badge">RESULT: DELIVERED</span>', page)
        self.assertIn('class="badge badge-lg badge-success"', page)
        for heading in REPORT_SECTIONS:
            self.assertIn(f'<h2 class="card-title">{heading}</h2>', page)
        self.assertIn('<span class="badge badge-success">passed</span>', page)
        self.assertIn('<span class="badge badge-warning">medium</span>', page)
        self.assertIn("<code>path/to/file</code>", page)

    def test_plan_goal_scope_and_decisions_are_embedded_collapsibly(self):
        page = self.render_template()
        match = re.search(r'<details class="collapse[^"]*plan">(.*?)</details>', page, re.S)
        self.assertIsNotNone(match)
        plan = match.group(1)
        self.assertIn("Plan: RF-0001 Example rapid feature", plan)
        for heading in ("Goal", "Scope", "Decisions"):
            self.assertIn(f"<h3>{heading}</h3>", plan)
        self.assertIn("State the outcome and how success is recognized.", plan)
        self.assertIn("List what this feature delivers.", plan)
        self.assertIn("Decision, rationale, and who made it.", plan)
        self.assertNotIn("Non-goals", plan)

    def test_no_external_resource_references(self):
        page = self.render_template()
        self.assertIsNone(re.search(r"\b(?:src|href|srcset|action)\s*=", page, re.I))
        self.assertIsNone(re.search(r"url\(\s*[\"']?https?:", page, re.I))
        self.assertIsNone(re.search(r"@import", page, re.I))
        self.assertIsNone(re.search(r"<(?:link|img|iframe|object|embed)\b", page, re.I))
        # The only script is the inline theme toggle, with no attributes.
        self.assertEqual(re.findall(r"<script\b[^>]*>", page, re.I), ["<script>"])
        # The only http(s) strings are XML namespace identifiers inside the
        # stylesheet's inline data: SVGs; outside the stylesheet there are none.
        self.assertLessEqual(set(re.findall(r"https?://[^\s'\"%)]+", page)), NAMESPACE_URIS)
        outside_css = re.sub(r'<style id="daisyui-styles">.*?</style>', "", page, flags=re.S)
        self.assertNotRegex(outside_css, r"https?://")

    def test_markdown_text_is_escaped(self):
        report = REPORT_TEMPLATE.replace("title: Example rapid feature", 'title: Fix <b>"bold"</b> & more')
        report = report.replace(
            "## Findings\n\n",
            "## Findings\n\n- <script>alert(1)</script> and `<img src=x>`\n\n",
        )
        plan = PLAN_TEMPLATE.replace("State the outcome", "<iframe>State the outcome")
        page = self.render_template(report=report, plan=plan)
        self.assertNotIn("<script>alert(1)</script>", page)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt;", page)
        self.assertIn("<code>&lt;img src=x&gt;</code>", page)
        self.assertIn("Fix &lt;b&gt;&quot;bold&quot;&lt;/b&gt; &amp; more", page)
        self.assertIn("&lt;iframe&gt;State the outcome", page)
        without_theme_script = re.sub(r"<script>.*?</script>", "", page, count=1, flags=re.S)
        self.assertIsNone(re.search(r"<(?:script|img|iframe)\b", without_theme_script))

    def test_markdown_subset(self):
        report = REPORT_TEMPLATE.replace(
            "## Findings\n\n- Record discoveries, risks, and decisions made during implementation, or write `None`.\n",
            "## Findings\n\n### Risk notes\n\nFirst line\ncontinues here with `code`.\n\n"
            "- outer item\n  - nested item\n- [ ] open task\n- [x] done task\n\n"
            "| Name | Value |\n| --- | --- |\n| a \\| b | `x` |\n\n"
            "See [the plan](README.md).\n",
        )
        page = self.render_template(report=report)
        self.assertIn("<h3>Risk notes</h3>", page)
        self.assertIn("<p>First line continues here with <code>code</code>.</p>", page)
        self.assertIn("<li>outer item</li>", page)
        self.assertIn('<li style="margin-left: 1.5rem">nested item</li>', page)
        self.assertRegex(page, r'<input type="checkbox" class="checkbox checkbox-sm" disabled aria-label="not done"> '
                               r"<span>open task</span>")
        self.assertRegex(page, r'disabled checked aria-label="done"> <span>done task</span>')
        self.assertIn("<th>Name</th><th>Value</th>", page)
        self.assertIn("<td>a | b</td><td><code>x</code></td>", page)
        self.assertIn('the plan <span class="link-target">(README.md)</span>', page)

    def test_self_verified_review_with_null_reviewer_renders(self):
        report = set_key(set_key(REPORT_TEMPLATE, "review", "self-verified"), "reviewer", "null")
        report = report.replace("## Review\n\n", "## Review\n\n- Not independently reviewed. No subagents.\n")
        page = self.render_template(report=report)
        self.assertIn("<dt>Reviewer</dt><dd>null</dd>", page)
        self.assertIn('<p class="review-note">Not independently reviewed.</p>', page)

    def test_no_pending_issues_row(self):
        report = REPORT_TEMPLATE.replace(
            "| Describe each unresolved or out-of-scope issue | medium | BL-0001 |", "| None | - | - |"
        )
        page = self.render_template(report=report)
        self.assertIn("<td>None</td><td>-</td><td>-</td>", page)

    def test_partial_and_not_delivered_results(self):
        partial = REPORT_TEMPLATE.replace("RESULT: DELIVERED\n", "RESULT: PARTIAL\n").replace(
            "| passed | Output summary or file reference |",
            "| passed | Output summary or file reference |\n| Second | `x` | failed | log |",
        )
        self.assertIn("badge-warning\" id=\"result-badge\">RESULT: PARTIAL", self.render_template(report=partial))
        failed = REPORT_TEMPLATE.replace("RESULT: DELIVERED\n", "RESULT: NOT_DELIVERED\n").replace(
            "manual method | passed |", "manual method | not run |"
        )
        self.assertIn("RESULT: NOT_DELIVERED", self.render_template(report=failed))

    def test_marked_existing_page_is_replaced(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = make_folder(temp)
            (folder / "report.html").write_text(f"<!doctype html>\n{renderer.MARKER}\nold", encoding="utf-8")
            code, _, err = run(folder)
            self.assertEqual(code, 0, err)
            self.assertNotIn("\nold", (folder / "report.html").read_text(encoding="utf-8"))
            self.assertEqual(sorted(path.name for path in folder.iterdir()), ["README.md", "report.html", "report.md"])

    def test_command_line_entry_point(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = make_folder(temp)
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(folder)], capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("report.html", result.stdout)
            self.assertTrue((folder / "report.html").is_file())


class RefusalTests(unittest.TestCase):
    def assertRefused(self, folder, *expected):
        code, _, err = run(folder)
        self.assertNotEqual(code, 0)
        self.assertIn("nothing was written", err)
        for text in expected:
            self.assertIn(text, err)
        self.assertFalse((folder / "report.html").exists())
        self.assertEqual([path.name for path in folder.iterdir() if path.name.startswith(".report-")], [])
        return err

    def refuse_report(self, report, *expected, **kwargs):
        with tempfile.TemporaryDirectory() as temp:
            return self.assertRefused(make_folder(temp, report=report, **kwargs), *expected)

    def test_each_missing_frontmatter_key(self):
        for key in REPORT_KEYS:
            with self.subTest(key=key):
                report = re.sub(rf"^{key}:.*\n", "", REPORT_TEMPLATE, count=1, flags=re.M)
                self.refuse_report(report, f"missing frontmatter key: {key}")

    def test_missing_frontmatter_block_names_every_key(self):
        report = REPORT_TEMPLATE.split("---\n", 2)[2]
        err = self.refuse_report(report, "missing YAML frontmatter")
        for key in REPORT_KEYS:
            self.assertIn(f"missing frontmatter key: {key}", err)

    def test_empty_required_value(self):
        self.refuse_report(set_key(REPORT_TEMPLATE, "branch", ""), "empty frontmatter key: branch")

    def test_each_missing_section(self):
        for heading in REPORT_SECTIONS:
            with self.subTest(section=heading):
                self.refuse_report(drop_section(REPORT_TEMPLATE, heading), f"missing section: ## {heading}")

    def test_sections_out_of_order(self):
        findings = re.search(r"^## Findings\n.*?(?=^## )", REPORT_TEMPLATE, re.S | re.M).group(0)
        report = drop_section(REPORT_TEMPLATE, "Findings").replace("## Outcome\n", findings + "## Outcome\n")
        self.refuse_report(report, "sections out of order")

    def test_unexpected_and_duplicate_sections(self):
        self.refuse_report(REPORT_TEMPLATE + "\n## Notes\n\nExtra.\n", "unexpected section: ## Notes")
        self.refuse_report(REPORT_TEMPLATE + "\n## Findings\n\nAgain.\n", "duplicate section: ## Findings")

    def test_empty_section(self):
        report = re.sub(r"(## Changes\n).*?(?=## Findings)", r"\1\n", REPORT_TEMPLATE, flags=re.S)
        self.refuse_report(report, "empty section: ## Changes")

    def test_invalid_result_line(self):
        cases = {
            "lowercase": "RESULT: delivered",
            "unknown value": "RESULT: DONE",
            "missing": "Summary without a result line.",
            "decorated": "**RESULT: DELIVERED**",
        }
        for name, line in cases.items():
            with self.subTest(case=name):
                report = REPORT_TEMPLATE.replace("RESULT: DELIVERED", line, 1)
                self.refuse_report(report, "## Outcome must start with a RESULT: line")

    def test_result_line_must_come_first(self):
        report = REPORT_TEMPLATE.replace("## Outcome\n\nRESULT: DELIVERED", "## Outcome\n\nIntro.\n\nRESULT: DELIVERED")
        self.refuse_report(report, "## Outcome must start with a RESULT: line")

    def test_invalid_review_value(self):
        self.refuse_report(set_key(REPORT_TEMPLATE, "review", "peer"), "invalid review 'peer'")

    def test_reviewer_rules(self):
        self.refuse_report(
            set_key(REPORT_TEMPLATE, "reviewer", "null"), "reviewer must name the reviewing subagent"
        )
        self_verified = set_key(REPORT_TEMPLATE, "review", "self-verified")
        self.refuse_report(self_verified, "reviewer must be null when review is self-verified")
        skipped = set_key(set_key(REPORT_TEMPLATE, "review", "skipped"), "reviewer", "null")
        skipped = re.sub(r"(## Review\n).*?(?=## Pending)", r"\1\n- Reviewer: none.\n\n", skipped, flags=re.S)
        self.refuse_report(skipped, "## Review must state 'Not independently reviewed.' when review is skipped")

    def test_invalid_status_and_id(self):
        self.refuse_report(set_key(REPORT_TEMPLATE, "status", "Done"), "invalid status 'Done'")
        self.refuse_report(set_key(REPORT_TEMPLATE, "id", "RF-1"), "invalid id 'RF-1'")

    def test_invalid_check_result(self):
        report = REPORT_TEMPLATE.replace("manual method | passed |", "manual method | ok |")
        self.refuse_report(report, "## Acceptance checks row 1: invalid result 'ok'")

    def test_table_headers_must_match(self):
        report = REPORT_TEMPLATE.replace("| Check | Command / method |", "| Check | Command |")
        self.refuse_report(report, "## Acceptance checks table header must be exactly")
        report = REPORT_TEMPLATE.replace("| Issue | Severity | Backlog |", "| Issue | Priority | Backlog |")
        self.refuse_report(report, "## Pending issues table header must be exactly")

    def test_missing_table_and_wrong_cell_count(self):
        report = re.sub(r"\| Check \|.*?Output summary or file reference \|\n", "- no table\n", REPORT_TEMPLATE, flags=re.S)
        self.refuse_report(report, "## Acceptance checks is missing its table")
        report = REPORT_TEMPLATE.replace("`command` or manual method | passed |", "passed |")
        self.refuse_report(report, "## Acceptance checks row 1 has 3 cells; expected 4")

    def test_result_must_match_check_results(self):
        report = REPORT_TEMPLATE.replace("manual method | passed |", "manual method | failed |")
        self.refuse_report(report, "RESULT: DELIVERED requires every acceptance check to be passed")
        report = report.replace("RESULT: DELIVERED", "RESULT: PARTIAL")
        self.refuse_report(report, "RESULT: NOT_DELIVERED is required when no acceptance check passed")

    def test_pending_issue_rules(self):
        row = "| Describe each unresolved or out-of-scope issue | medium | BL-0001 |"
        self.refuse_report(REPORT_TEMPLATE.replace(row, "| Bug | urgent | - |"), "invalid severity 'urgent'")
        self.refuse_report(REPORT_TEMPLATE.replace(row, "| Bug | low | 42 |"), "invalid backlog '42'")
        self.refuse_report(
            REPORT_TEMPLATE.replace(row, row + "\n| None | - | - |"), "row must be the only row"
        )
        self.refuse_report(REPORT_TEMPLATE.replace(row + "\n", ""), "## Pending issues table has no rows")

    def test_every_problem_is_reported_at_once(self):
        report = set_key(REPORT_TEMPLATE, "review", "peer").replace("RESULT: DELIVERED", "RESULT: maybe")
        report = drop_section(report, "Findings")
        err = self.refuse_report(report, "invalid review 'peer'", "RESULT: line", "missing section: ## Findings")
        self.assertIn("3 problem(s)", err)

    def test_missing_report_or_plan(self):
        self.refuse_report(None, "report.md not found")
        self.refuse_report(REPORT_TEMPLATE, "plan README.md not found", plan=None)

    def test_plan_requires_goal_scope_and_decisions(self):
        for heading in ("Goal", "Scope", "Decisions"):
            with self.subTest(section=heading):
                plan = drop_section(PLAN_TEMPLATE, heading)
                self.refuse_report(REPORT_TEMPLATE, f"README.md (plan): missing section: ## {heading}", plan=plan)

    def test_report_and_plan_ids_must_match(self):
        plan = set_key(PLAN_TEMPLATE, "id", "RF-0002")
        self.refuse_report(REPORT_TEMPLATE, "id RF-0001 does not match the plan id RF-0002", plan=plan)

    def test_project_name_is_required(self):
        self.refuse_report(REPORT_TEMPLATE, "Project name: <name>", project_line=None)
        self.refuse_report(REPORT_TEMPLATE, "Project name: <name>", project_line="Project name: <name>")
        self.refuse_report(REPORT_TEMPLATE, "Project name: <name>", project_line="No name here")

    def test_folder_outside_workspace(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "RF-0001--x"
            folder.mkdir()
            (folder / "report.md").write_text(REPORT_TEMPLATE, encoding="utf-8")
            (folder / "README.md").write_text(PLAN_TEMPLATE, encoding="utf-8")
            self.assertRefused(folder, "not inside a trinary-workspace/ directory")

    def test_unmarked_existing_page_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = make_folder(temp)
            existing = folder / "report.html"
            existing.write_text("<p>hand-written</p>", encoding="utf-8")
            code, _, err = run(folder)
            self.assertNotEqual(code, 0)
            self.assertIn("refusing to overwrite a page not generated by this renderer", err)
            self.assertEqual(existing.read_text(encoding="utf-8"), "<p>hand-written</p>")

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_symlinked_page_is_not_followed(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = make_folder(temp)
            target = Path(temp) / "elsewhere.html"
            target.write_text(renderer.MARKER, encoding="utf-8")
            (folder / "report.html").symlink_to(target)
            code, _, err = run(folder)
            self.assertNotEqual(code, 0)
            self.assertIn("refusing to overwrite a symlink", err)
            self.assertEqual(target.read_text(encoding="utf-8"), renderer.MARKER)

    def test_usage(self):
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            self.assertEqual(renderer.main([]), 2)
        self.assertIn("Usage: render_report.py <RF folder>", err.getvalue())

    def test_command_line_refusal_exit_code(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = make_folder(temp, report=drop_section(REPORT_TEMPLATE, "Review"))
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(folder)], capture_output=True, text=True, check=False
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("missing section: ## Review", result.stderr)
            self.assertFalse((folder / "report.html").exists())


class PackagingTests(unittest.TestCase):
    def test_only_standard_library_imports(self):
        allowed = {"html", "os", "re", "sys", "tempfile", "pathlib"}
        tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                imported.add((node.module or "").split(".")[0])
        self.assertLessEqual(imported, allowed)

    def test_assets_are_bundled_with_the_skill(self):
        assets = SKILL / "assets" / "report"
        self.assertTrue((assets / "daisyui-5.7.50.css").is_file())
        self.assertTrue((assets / "LICENSE-daisyui-MIT.txt").is_file())
        self.assertTrue((assets / "README.md").is_file())

    def test_skill_templates_match_references(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for template in (REPORT_TEMPLATE, PLAN_TEMPLATE):
            self.assertIn("```markdown\n" + template + "```\n", skill)


if __name__ == "__main__":
    unittest.main()
