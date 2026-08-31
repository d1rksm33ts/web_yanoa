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
        self.heading_levels = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.append(attributes["href"])
        if tag == "img":
            self.images.append(attributes)
        if tag == "link" and attributes.get("rel") == "stylesheet":
            self.stylesheets.append(attributes.get("href"))
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
            "Astrophotographer",
            "Radio amateur",
            "mailto:dirk.smeets@yanoa.be",
            "tel:+32476691902",
        ):
            self.assertIn(text, self.source)

        self.assertTrue((ROOT / "site" / "assets" / "dirk.jpg").is_file())
        stylesheet = (ROOT / "site" / "assets" / "styles.css").read_text(
            encoding="utf-8"
        )
        self.assertIn('/assets/dirk.jpg', stylesheet)

    def test_unrelated_hosted_sites_are_absent(self):
        lowered = self.source.lower()
        for excluded in ("dechapper", "chapper.be", "zonhoven-united"):
            self.assertNotIn(excluded, lowered)

    def test_assets_are_local(self):
        self.assertEqual(self.parser.stylesheets, ["/assets/styles.css"])
        for image in self.parser.images:
            self.assertTrue(image.get("src", "").startswith("/assets/"))
            self.assertIn("alt", image)

    def test_document_has_one_primary_heading(self):
        self.assertEqual(self.source.count("<h1"), 1)
        self.assertEqual(self.parser.heading_levels[0], 1)

    def test_no_runtime_javascript(self):
        self.assertNotIn("<script", self.source.lower())


if __name__ == "__main__":
    unittest.main()
