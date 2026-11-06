"""Use the supplied vector artwork without raster filters or clipping."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ET.register_namespace('', 'http://www.w3.org/2000/svg')
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')
ET.register_namespace('html', 'http://www.w3.org/1999/xhtml')

def badge_svg(light=False):
    root = ET.fromstring((Path(__file__).parent / 'logic/assets/light-quality-badges.svg').read_text())
    for element in root.iter():
        assert element.tag.rsplit('}', 1)[-1] != 'script'
        assert not any(key.lower().startswith('on') for key in element.attrib)
        for key, value in element.attrib.items():
            if key.rsplit('}', 1)[-1] == 'href':
                assert value.startswith('#')
    if light:
        # Visible lettering only: DC48V, CRI and the white Bridgelux lettering.
        # Keep the LED badge's white letters/border and all mask geometry intact.
        for index in (0, 3, 10):
            assert root[index].get('fill') == 'white'
            root[index].set('fill', '#1d2731')
        assert root[12].get('stroke') == 'white'
        root[12].set('stroke', '#1d2731')
    root.set('class', 'quality-badges' if light else 'hero-badges')
    root.set('role', 'img')
    root.set('aria-label', 'DC48V · CRI 90+ · LED · Bridgelux · 3000К / 4000К')
    text = ET.tostring(root, encoding='unicode', short_empty_elements=False)
    text = text.replace('<html:div', '<div xmlns="http://www.w3.org/1999/xhtml"').replace('</html:div>', '</div>')
    # The two copies must not share paint/mask IDs in the same document.
    prefix = 'quality-' if light else 'hero-'
    for ident in sorted(re.findall(r'\bid="([^"]+)"', text), key=len, reverse=True):
        text = text.replace('id="'+ident+'"', 'id="'+prefix+ident+'"')
        text = text.replace('#'+ident, '#'+prefix+ident)
    return text
