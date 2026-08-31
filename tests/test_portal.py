from html.parser import HTMLParser
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "site" / "index.html"


class PortalParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.stylesheets = []
        self.scripts = []
        self.heading_levels = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "img":
            self.images.append(attributes)
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(attributes.get("href"))
        if tag == "script" and "src" in attributes:
            self.scripts.append(attributes["src"])
        if tag in {"h1", "h2", "h3"}:
            self.heading_levels.append(int(tag[1]))


class PortalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = INDEX.read_text(encoding="utf-8")
        cls.parser = PortalParser()
        cls.parser.feed(cls.source)

    def test_confirmed_yanoa_destinations_are_present(self):
        expected = {
            "https://home.yanoa.be",
            "https://racing.yanoa.be",
            "https://astro.yanoa.be",
            "https://telemetry.yanoa.be",
        }
        self.assertTrue(expected.issubset(set(self.parser.links)))

    def test_personal_identity_and_contact_are_primary_content(self):
        for text in (
            "Dirk Smeets",
            "Engineer",
            "Teacher",
            "Astrophotographer",
            "Radio Amateur",
            "mailto:dirk.smeets@yanoa.be",
            "https://www.instagram.com/d1rksm33ts/",
            "https://www.astrobin.com/users/d1rksm33ts/",
        ):
            self.assertIn(text, self.source)

        self.assertNotIn("tel:", self.source)
        self.assertNotIn("Technologist", self.source)

        self.assertTrue((ROOT / "site" / "assets" / "dirk.jpg").is_file())
        stylesheet = (ROOT / "site" / "assets" / "site.css").read_text(
            encoding="utf-8"
        )
        self.assertIn('/assets/dirk.jpg', stylesheet)

    def test_unrelated_hosted_sites_are_absent(self):
        lowered = self.source.lower()
        for excluded in ("dechapper", "chapper.be", "zonhoven-united"):
            self.assertNotIn(excluded, lowered)

    def test_assets_are_local(self):
        self.assertEqual(self.parser.stylesheets, ["/assets/site.css"])
        for image in self.parser.images:
            self.assertTrue(image.get("src", "").startswith("/assets/"))
            self.assertIn("alt", image)

    def test_document_has_one_primary_heading(self):
        self.assertEqual(self.source.count("<h1"), 1)
        self.assertEqual(self.parser.heading_levels[0], 1)

    def test_animation_scripts_are_local(self):
        self.assertEqual(
            self.parser.scripts,
            ["/assets/typed-2.0.12.min.js", "/assets/site.js"],
        )
        script = (ROOT / "site" / "assets" / "site.js").read_text(encoding="utf-8")
        self.assertIn("typeSpeed: 100", script)
        self.assertIn("backSpeed: 50", script)
        self.assertIn("backDelay: 2000", script)
        self.assertIn('history.scrollRestoration = "manual"', script)


if __name__ == "__main__":
    unittest.main()
