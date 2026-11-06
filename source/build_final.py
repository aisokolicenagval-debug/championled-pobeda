# coding: utf-8
"""Build the approved local/public HTML design from the editable content prototype.
No storefront or catalog mutation. Only public assets are embedded.
"""
from pathlib import Path
import re,json,html,shutil,base64
from quality_icon_assets import badge_svg
from hero_content import HERO_COPY, benefits_markup
from installation_section import render_installation
from control_section import render_control
ROOT=Path(__file__).resolve().parent
s=(ROOT/'logic/landing.html').read_text()
slider_start=s.index('const lightTrack=');slider_end=s.index("$('menu').addEventListener",slider_start)
s=s[:slider_start]+(ROOT/'light-slider.js').read_text()+'\n'+s[slider_end:]
a=json.loads((ROOT/'final-assets/embedded.json').read_text());assets=a['assets'];st=a['settings'];photos=a['products']
assets['local:hero-enhanced-v2.png']='data:image/png;base64,'+base64.b64encode((ROOT/'logic/assets/hero-enhanced-v2.png').read_bytes()).decode()
for case_index in range(1,5):
 assets[f'local:case-{case_index}.jpg']='data:image/jpeg;base64,'+base64.b64encode((ROOT/'logic/assets'/f'case-{case_index}.jpg').read_bytes()).decode()
def image(v):
 u=v.get('filePath') if isinstance(v,dict) else v
 return assets[u]
def img(v,cls,alt='',eager=False):return '<img class="'+cls+'" src="'+image(v)+'" alt="'+html.escape(alt,quote=True)+'" '+('fetchpriority="high" loading="eager"' if eager else 'loading="lazy"')+' decoding="async">'
# Use the genuine four font files; retain a portable HTML with no image/font requests.
fonts=a['fonts']
# The reference site overloads one family name with both body and display faces.
# Explicit aliases keep document headings and labels from swapping typefaces.
font_aliases=[]
for block in re.findall(r'@font-face\s*\{.*?\}',a['fonts'],re.S):
 weight=re.search(r'font-weight:\s*(\d+)',block).group(1)
 alias='Science' if weight=='600' else 'Geist'
 named=block.replace('"Geist_Science"','"'+alias+'"')
 if alias=='Science':named=re.sub(r'font-weight:\s*600','font-weight: 300 700',named)
 font_aliases.append(named)
fonts+='\n'+'\n'.join(font_aliases)
for u in re.findall(r"url\('([^']+)'\)",fonts):fonts=fonts.replace(u,assets[u])
s=re.sub(r'<style>.*?</style>','<style>\n'+fonts+'\n'+(ROOT/'final-style.css').read_text()+'\n'+(ROOT/'layout-system.css').read_text()+'\n</style>',s,count=1,flags=re.S)
s=s.replace('<meta name="robots" content="noindex,nofollow">','<meta name="robots" content="noindex,nofollow"><meta name="theme-color" content="#1d2731"><meta name="description" content="Магнитная трековая система Победа 48В от ChampionLED. Сравните Про и Эко, выберите светильники и компоненты системы.">')
header='''<header class="site-header"><div class="wrap head-inner"><a class="logo" href="#top">'''+img(a['logo'],'brand-logo','CHAMPIONLED',True)+'''</a><a class="btn small header-catalog" href="https://championled.ru/catalog/pobeda-pro" target="_blank" rel="noopener">Каталог</a><a class="header-phone" href="tel:+78003503085">8 (800) 350-30-85</a><a class="header-mail" href="mailto:order@championled.ru">order@championled.ru</a><a class="btn small" href="#shop">Купить компоненты</a><button type="button" class="menu" id="menu" aria-expanded="false" aria-controls="nav">Меню</button></div><nav class="nav" id="nav" aria-label="Разделы страницы"><a href="#editions">Про и Эко</a><a href="#shop">Товары</a><a href="#light">Светильники</a><a href="#connections">Монтаж и схемы</a><a href="#documents">Документы</a><a href="#cases">Кейсы</a><a href="#faq">Вопросы</a></nav></header>'''
s=re.sub(r'<header class="site-header">.*?</header>',lambda m:header,s,count=1,flags=re.S)
hero='''<section class="hero">'''+img('local:hero-enhanced-v2.png','hero-backdrop','Магнитная трековая система Победа в интерьере',True)+'''<div class="wrap hero-inner"><div class="hero-copy"><div class="eyebrow">CHAMPIONLED / Магнитная система 48В</div><h1>Магнитная трековая система<br>«Победа» 48В</h1><p>'''+HERO_COPY+'''</p><div class="actions"><a href="#shop" class="btn">Купить компоненты</a><a href="#editions" class="btn outline">Сравнить Про и Эко</a></div>'''+badge_svg(False)+'''</div></div></section>'''
s=re.sub(r'<section class="hero">.*?</section>',lambda m:hero,s,count=1,flags=re.S)
# Five approved purchase benefits replace the repeated technical summary.
facts_markup=benefits_markup()
a0=s.index('<div class="wrap facts"');b=s.index('<section',a0);s=s[:a0]+facts_markup+'\n'+s[b:]
# User-provided edition photos replace the separate profile and mounting drawings.
import base64
for filename in ['edition-pro-labeled.png','edition-eco.png','document-catalog.png','document-instructions.png','document-technical.png']:
 path=ROOT/'logic/assets'/filename
 uri='data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()
 s=s.replace('src="assets/'+filename+'"','src="'+uri+'"')
# Preserve the six image-led cards; embed their existing image assets.
for u,uri in assets.items():
 if u.startswith('https:'):s=s.replace('src="'+u+'"','src="'+uri+'"')
s=s.replace('<span data-quality-icon-strip></span>',badge_svg(True))
# Quality of light gets the existing full-size interior image.
s=re.sub(r'<div class="media quality-interior".*?</div>',lambda m:img(st['s09']['image'],'quality-interior','Освещение Победа в жилом интерьере'),s,count=1,flags=re.S)
# Connection map is separate from installing or moving a luminaire.
start=s.index('<div class="media scheme-image">');end=s.index('</div>',start)+6
s=s[:start]+'<div class="scheme-visual"><a id="schemeZoom" href="assets/pro-connection.jpg" aria-label="Увеличить схему соединения" aria-haspopup="dialog" aria-controls="schemeDialog"><div class="scheme-copy" id="schemeCopy" hidden><ul><li>Прямые участки и углы 90°</li><li>Встраиваемый монтаж</li><li>Встроенный блок питания</li></ul></div><div class="scheme-art"><picture><source id="schemeMobile" media="(max-width:600px)"><img id="schemeDiagram" alt="Схема соединения компонентов Победа Про"></picture></div></a><p class="scheme-zoom-hint">Нажмите на схему, чтобы открыть её крупно.</p></div>'+s[end:]
start=s.index('<div class="install-row">');end=s.index('</section>',start)
# Retain the scheme section wrap end; move the installation content into its own section.
s=s[:start]+'</div></section>\n'+s[end+10:]
installation_photo='data:image/png;base64,'+base64.b64encode((ROOT/'logic/assets/installation-magnetic-lock.png').read_bytes()).decode()
install=render_installation(img,st,installation_photo)
pos=s.index('<section class="section section-anchor" id="control">');s=s[:pos]+install+s[pos:]
# Reference photographs and protocol marks, with semantically matched control groups.
s=re.sub(r'<section class="section section-anchor" id="control">.*?</section>',lambda m:render_control(ROOT),s,count=1,flags=re.S)
# Replace gallery placeholders with existing interior photographs, without invented project claims.
for label,photo in [('Гостиная',st['s11']['image1']),('Офис',st['s11']['image2']),('Магазин / шоурум',st['s02']['image2'])]:s=s.replace('<div class="media"><span class="media-label">'+label+'</span></div>',img(photo,'gallery-photo',label+' — пример применения системы Победа'))
# Case captions remain placeholders as requested; no invented project names or URLs.
for case_index in range(1,5):
 s=s.replace('<span data-case-image="'+str(case_index)+'"></span>',img(f'local:case-{case_index}.jpg','case-photo','Пример освещения Победа Про в интерьере '+str(case_index)))
# Same current Kit CTA composition; the new message routes project work to LEDMONSTER only.
ledmonster_logo='data:image/png;base64,'+base64.b64encode((ROOT/'logic/assets/ledmonster-cta-logo.png').read_bytes()).decode()
project='''<section class="project" id="project"><div class="wrap"><div class="consultation-cta-kit__inner"><div class="consultation-cta-kit__media">'''+img(a['cta']['imageSettings']['image'],'consultation-cta-kit__image','Команда группы LEDMONSTER в шоуруме')+'''</div><div class="consultation-cta-kit__content"><img class="consultation-cta-kit__logo" src="'''+ledmonster_logo+'''" alt="LEDMONSTER" width="1000" height="132"><div class="project-kicker">Проектное освещение / LEDMONSTER</div><h2 class="consultation-cta-kit__title">Нужна консультация<br>по световому проекту?</h2><p class="consultation-cta-kit__text">Если для объекта нужен светотехнический расчёт, индивидуальное решение или комплексная работа со светом, расскажите о задаче команде LEDMONSTER.</p><div class="consultation-cta-kit__actions"><a class="btn" href="https://ledmonster.ru/" target="_blank" rel="noopener">Обсудить проект с LEDMONSTER</a></div></div></div></div></section>'''
s=re.sub(r'<section class="project">.*?</section>','',s,count=1,flags=re.S)
faq_start=s.index('<section class="section" id="faq">');s=s[:faq_start]+project+'\n'+s[faq_start:]
# End the landing with the FAQ itself.
faq_start=s.index('<section class="section" id="faq">');faq_end=s.index('</section>',faq_start)
chunk=s[faq_start:faq_end];chunk=re.sub(r'<div class="center more">.*?</div>','',chunk,flags=re.S);s=s[:faq_start]+chunk+s[faq_end:]
footer='''<footer class="footer"><div class="wrap"><div class="footer-inner"><div><a class="logo" href="#top">'''+img(a['invertedLogo'],'brand-logo','CHAMPIONLED')+'''</a><p>Современный функциональный свет для квартир, домов и коммерческих пространств.</p></div><div class="footer-contact"><a href="tel:+78003503085">8 (800) 350-30-85</a><a href="mailto:order@championled.ru">order@championled.ru</a><a href="https://championled.ru/contacts" target="_blank" rel="noopener">Контакты и шоурум ↗</a></div><div class="footer-links"><a href="https://championled.ru/catalog/pobeda-pro" target="_blank" rel="noopener">Каталог</a><a href="https://championled.ru/o-brende" target="_blank" rel="noopener">О бренде</a><a href="https://championled.ru/payment" target="_blank" rel="noopener">Оплата</a><a href="https://championled.ru/delivery" target="_blank" rel="noopener">Доставка</a><a href="https://championled.ru/return" target="_blank" rel="noopener">Гарантия</a><a href="https://ledmonster.ru/" target="_blank" rel="noopener">LEDMONSTER ↗</a></div></div><div class="footer-bottom">CHAMPIONLED · «Победа» · HTML-прототип.</div></div></footer>'''
s=re.sub(r'<footer class="footer">.*?</footer>',lambda m:footer,s,count=1,flags=re.S)
# Dynamic photo and diagram rendering reuses the real storefront assets.
connection_pro='data:image/png;base64,'+base64.b64encode((ROOT/'logic/assets/pro-connection-clean.png').read_bytes()).decode()
connection_eco='data:image/png;base64,'+base64.b64encode((ROOT/'logic/assets/eco-connection-clean.png').read_bytes()).decode()
media={'mounts':{},'diagramPro':connection_pro,'diagramProMobile':connection_pro,'diagramEco':connection_eco,'productImages':{k:image(v) for k,v in photos.items()},'lightImages':{st['s08']['name'+str(i)]:image(st['s08']['product'+str(i)]) for i in range(1,7)},'controlImages':[image(st['s10']['image1']),image(st['s10']['image2']),image(st['s10']['image3'])],'ecoProduct':image('local:eco-profile.png'),'ecoMount':image('local:eco-interior.jpg'),'ecoMountDiagram':'data:image/png;base64,'+base64.b64encode((ROOT/'logic/assets/eco-mount-profile-corrected-v4.png').read_bytes()).decode()}
for key,i in [('surface',1),('suspended',2),('inset',3)]:media['mounts'][key]={'photo':image(st['s03']['image'+str(i)]),'diagram':image(st['s03']['diagram'+str(i)]),'lead':st['s03']['card'+str(i)+'Lead'],'text':st['s03']['card'+str(i)+'Text']}
s=s.replace("const state={",'const finalMedia='+json.dumps(media,ensure_ascii=False,separators=(',',':'))+';\nconst state={',1)
# Include SKU information in component shelf cards for exact photo mapping.
s=s.replace("params:['48В'],price:v.price,href:v.href}","params:['48В'],price:v.price,href:v.href,sku:v.sku}")
needle="function renderShop(){";idx=s.index(needle)
helpers="""function shelfImage(p){if(p.slug)return finalMedia.lightImages[p.name];if(p.sku){if(finalMedia.productImages[p.sku])return finalMedia.productImages[p.sku];const prefix=p.sku.split('-').slice(0,3).join('-')+'-';const key=Object.keys(finalMedia.productImages).find(k=>k.startsWith(prefix));if(key)return finalMedia.productImages[key];if(p.sku.startsWith('01-'))return finalMedia.ecoProduct;}return finalMedia.lightImages['Слава'];}\n"""
s=s[:idx]+helpers+s[idx:]
s=s.replace("<span class=\"media-label\">'+esc(p.name)+'</span></a>","<img src=\"'+shelfImage(p)+'\" alt=\"'+esc(p.name)+'\" loading=\"lazy\"></a>",1)
start=s.index('function renderSystem()');end=s.index('function renderSpecs(',start)
render='''function geometryIcon(name){const paths={'Прямая':'M8 32H82','Г-образная':'M16 50V12H75','П-образная':'M10 50V12H80V50','Радиусная':'M18 50V30A25 25 0 0 1 68 30V50','Комбинированная':'M10 50V13H55A20 20 0 0 1 55 53H40','Квадрат':'M18 10H68V54H18Z','Прямоугольник':'M8 17H82V49H8Z'};return '<svg viewBox="0 0 90 65" aria-hidden="true"><path d="'+(paths[name]||paths['Прямая'])+'" fill="none" stroke="#1d2731" stroke-width="2.5"/></svg>';}
function renderSystem(){const pro=state.edition==='pro',ed=pro?'Про':'Эко';const modes=pro?[['surface','Накладной','На поверхности потолка или стены.'],['suspended','Подвесной','Шинопровод ниже потолка на подвесах.'],['inset','Встраиваемый','Интеграция в потолочную конструкцию.']]:[['inset','Встраиваемый','Пластиковый шинопровод Эко интегрируется в потолочную конструкцию.']];$('mountingCards').classList.toggle('single',!pro);$('mountingCards').innerHTML=modes.map(([k,n,t])=>'<article class="mounting-card"><img class="mounting-photo" src="'+(pro?finalMedia.mounts[k].photo:finalMedia.ecoMount)+'" alt="'+n+' монтаж системы Победа" loading="lazy"><div class="mounting-body"><h3>'+n+'</h3><div class="mounting-detail"><img class="'+(pro?'mounting-profile':'mounting-profile mounting-profile-eco')+'" src="'+(pro?finalMedia.mounts[k].diagram:finalMedia.ecoMountDiagram)+'" alt="Схема: '+n.toLowerCase()+' монтаж"><div class="mounting-description"><p class="mounting-lead">'+esc(pro?finalMedia.mounts[k].lead:t)+'</p><p class="mounting-note">'+esc(pro?finalMedia.mounts[k].text:'Встраиваемый монтаж для прямых и угловых световых линий.')+'</p></div></div></div></article>').join('');$('geometry').innerHTML=(pro?['Прямая','Г-образная','П-образная','Радиусная','Комбинированная']:['Прямая','Г-образная','Квадрат','Прямоугольник']).map(x=>'<span class="geometry-item">'+geometryIcon(x)+x+'</span>').join('');renderScheme();}
function renderScheme(){const pro=(state.schemeEdition||state.edition)==='pro',ed=pro?'Про':'Эко';document.querySelectorAll('[data-scheme-edition]').forEach(link=>link.setAttribute('aria-current',String(link.dataset.schemeEdition===(state.schemeEdition||state.edition))));$('schemeTitle').textContent='Схема соединения «Победа '+ed+'»';$('schemeDescription').textContent=pro?'Прямые, угловые и радиусные линии. Накладной, подвесной и встраиваемый монтаж.':'Прямые участки и углы 90°. Только встраиваемый монтаж.';$('schemeCopy').hidden=false;$('schemeCopy').innerHTML='<ul>'+(pro?['Гибкая конфигурация','Простота монтажа','Надёжное соединение']:['Прямые участки и углы 90°','Встраиваемый монтаж','Встроенный блок питания']).map(text=>'<li>'+text+'</li>').join('')+'</ul>';$('schemeDiagram').src=pro?finalMedia.diagramPro:finalMedia.diagramEco;$('schemeDiagram').alt='Схема соединения компонентов Победа '+ed;$('schemeMobile').srcset=pro?finalMedia.diagramProMobile:finalMedia.diagramEco;$('schemeZoom').href='assets/'+(pro?'pro-connection-clean.png':'eco-connection-clean.png');const parts=pro?[['Шинопроводы Про','tracks'],['Углы и радиусные элементы','tracks'],['Соединители Про','parts'],['Питание и подключение','power']]:[['Шинопроводы Эко','tracks'],['Угловые элементы Эко','tracks'],['Соединители Эко','parts'],['Питание и подключение Эко','power']];$('schemeLegend').innerHTML=parts.map(([n,c])=>'<div class="scheme-item"><b>'+n+'</b><button type="button" class="text-link" data-open-category="'+c+'">К товарам →</button></div>').join('');}
'''
s=s[:start]+render+s[end:]
# Avoid the unresolved 100°/36° discrepancy for Acrobat between supplied manual and catalog.
s=s.replace("kind:'Поворотный рассеянный свет',desc:'Широкий световой пучок и поворотное исполнение.',params:['12Вт','100°','CRI >90']","kind:'Поворотный свет',desc:'Меняйте положение и направление светильника.',params:['12Вт','CRI >90']")
s=s.replace('id="cartTitle">Демонстрационная корзина','id="cartTitle">Корзина конфигурации').replace('Выбранные товары добавлены только в прототип. Заказ в магазине не создаётся.','Демонстрация: выбранные товары добавлены только в прототип. Заказ в магазине не создаётся.')
# Full-size schemes open in an accessible dialog with an explicit close action.
zoom_dialog='<dialog class="scheme-dialog" id="schemeDialog" aria-labelledby="schemeDialogTitle"><div class="scheme-dialog-header"><h2 id="schemeDialogTitle">Схема соединения</h2><button type="button" class="scheme-dialog-close" id="closeSchemeDialog" aria-label="Закрыть схему"><span aria-hidden="true">×</span></button></div><div class="scheme-dialog-pane"><img id="schemeDialogImage" alt=""></div></dialog>'
s=s.replace('<script>',zoom_dialog+'\n<script>',1)
zoom_script="""
const schemeDialog=$('schemeDialog');let schemeReturnScroll=0,schemeDialogTrigger=null;
$('schemeZoom').addEventListener('click',event=>{event.preventDefault();schemeReturnScroll=window.scrollY;schemeDialogTrigger=$('schemeZoom');$('closeSchemeDialog').setAttribute('aria-label','Закрыть схему');const pro=(state.schemeEdition||state.edition)==='pro';$('schemeDialogTitle').textContent=$('schemeTitle').textContent;$('schemeDialogImage').src=pro?finalMedia.diagramPro:finalMedia.diagramEco;$('schemeDialogImage').alt=$('schemeTitle').textContent;schemeDialog.showModal();document.body.classList.add('scheme-dialog-open');});

document.querySelectorAll('[data-edition-preview]').forEach(button=>button.addEventListener('click',()=>{schemeReturnScroll=window.scrollY;schemeDialogTrigger=button;const pro=button.dataset.editionPreview==='pro';$('schemeDialogTitle').textContent=pro?'Способы монтажа «Победа Про»':'Победа Эко в интерьере';const image=button.querySelector('img');$('schemeDialogImage').src=image.src;$('schemeDialogImage').alt=image.alt;$('closeSchemeDialog').setAttribute('aria-label','Закрыть изображение');schemeDialog.showModal();document.body.classList.add('scheme-dialog-open');}));
$('closeSchemeDialog').addEventListener('click',()=>schemeDialog.close());
schemeDialog.addEventListener('click',event=>{if(event.target===schemeDialog)schemeDialog.close();});
schemeDialog.addEventListener('close',()=>{document.body.classList.remove('scheme-dialog-open');schemeDialogTrigger?.focus({preventScroll:true});window.scrollTo({top:schemeReturnScroll,behavior:'instant'});});
"""
s=s.replace('render();\n})();',zoom_script+'\nrender();\n})();')
# Reuse the established contact-form fields for document requests.
s=s.replace('<script>',(ROOT/'document-request-dialog.html').read_text()+'\n<script>',1)
s=s.replace('render();\n})();',(ROOT/'document-request.js').read_text()+'\nrender();\n})();')
# Every static image should be embedded; dynamic images are in finalMedia.
assert not re.findall(r'<img[^>]+src="https?://',s),'External static image remains'
assert 'schemeImageLabel' not in s and 'copyConfiguration' not in s
s=s.replace('loading="lazy"','loading="eager"')
out=ROOT/'final';out.mkdir(exist_ok=True)
(out/'assets').mkdir(exist_ok=True)
for filename in ['pro-connection-clean.png','eco-connection-clean.png']:
 shutil.copyfile(ROOT/'logic/assets'/filename,out/'assets'/filename)
(out/'index.html').write_text(s)
(out/'ChampionLED_Pobeda_HTML_prototype.html').write_text(s)
(out/'.nojekyll').write_text('')
(ROOT/'final-review-check.js').write_text(re.search(r'<script>(.*?)</script>',s,re.S)[1])
print('Built final HTML:',len(s.encode()),'bytes')
