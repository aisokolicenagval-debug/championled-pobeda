"""Control cards merge the supplied reference artwork with the approved content."""
import base64
import html

def render_control(root):
    def uri(name, mime):
        return 'data:'+mime+';base64,'+base64.b64encode((root/'logic/assets'/name).read_bytes()).decode()
    strip=uri('control-protocol-strip.png','image/png')
    zigbee=uri('control-zigbee.png','image/png')
    def logo(data, box, cls, label, width, height):
        return '<svg class="control-protocol-logo '+cls+'" viewBox="'+box+'" role="img" aria-label="'+label+'"><defs><mask id="'+cls+'-mask" maskUnits="userSpaceOnUse" x="0" y="0" width="'+str(width)+'" height="'+str(height)+'" style="mask-type:luminance"><image href="'+data+'" width="'+str(width)+'" height="'+str(height)+'"></image></mask></defs><rect width="'+str(width)+'" height="'+str(height)+'" fill="white" mask="url(#'+cls+'-mask)"></rect></svg>'
    power='<svg class="control-mode-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M12 2v10M6 5.5a9 9 0 1 0 12 0"></path></svg>'
    dial='<svg class="control-mode-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"></circle><path d="m12 12 4-4M5.5 16.5h.01M18.5 16.5h.01"></path></svg>'
    badges=[
        power+'<span>ON/OFF</span>',
        logo(strip,'220 105 660 250','control-logo-dali','DALI',3546,443)+'<span class="control-badge-divider"></span>'+dial+'<span>0–10В</span>',
        logo(strip,'1520 150 675 150','control-logo-casambi','Casambi',3546,443)+'<span class="control-badge-divider"></span>'+logo(zigbee,'25 65 430 155','control-logo-zigbee','Zigbee',480,270),
    ]
    cards=[
        ('Базовое<br> управление','ON/OFF','Обычный выключатель для включения и выключения света.',3,'Магнитное трековое освещение в галерее'),
        ('Сценарии<br> и диммирование','0–10В / DALI','Проводное управление яркостью и группами светильников.',1,'Световые линии в современном жилом интерьере'),
        ('Умный<br> дом','Zigbee / Casambi','Беспроводные сценарии с совместимыми контроллерами и оборудованием.',2,'Трековое освещение в тёплом жилом интерьере'),
    ]
    out='''<section class="section section-anchor" id="control"><div class="wrap"><div class="section-head"><h2>От обычного выключателя<br> до умного дома</h2><p>Управляйте светом обычным выключателем, регулируйте яркость или объединяйте освещение в сценарии умного дома. Возможности зависят от совместимости светильников, плат и контроллеров.</p></div><div class="control-grid">'''
    for i,(title,protocol,text,photo,alt) in enumerate(cards):
        out+='<article class="control-card"><div class="control-visual"><img class="control-photo" src="'+uri('control-interior-'+str(photo)+'.jpg','image/jpeg')+'" alt="'+html.escape(alt)+'" loading="lazy"><div class="control-badge">'+badges[i]+'</div></div><div class="control-body"><h3>'+title+'</h3><div class="control-protocol">'+protocol+'</div><p>'+text+'</p></div></article>'
    return out+'</div></div></section>'
