"""Two-column installation story using the supplied photo and existing diagrams."""

def render_installation(image_fn, settings, photo_uri):
    section = '''<section class="section section-anchor" id="installation"><div class="wrap"><div class="section-head"><h2>Магнит и скрытый<br> механический замок</h2><p>Светильники легко устанавливать и перемещать. В системе «Победа» магнит помогает установить светильник в шинопровод, а скрытый механический замок удерживает его на месте.</p></div><div class="installation-layout"><div class="installation-feature"><button type="button" class="installation-photo-button" data-install-preview="Магнит и механический замок" aria-label="Увеличить изображение магнитного крепления" aria-haspopup="dialog" aria-controls="schemeDialog"><img src="'''+photo_uri+'''" alt="Магнитный адаптер светильника Победа перед установкой в шинопровод" width="1439" height="1620" loading="lazy"><span class="installation-photo-caption">Победа · магнитное крепление</span></button></div><ol class="installation-steps" aria-label="Установка и перемещение светильника">'''
    steps = [
        ('Поднести', 'Поднесите светильник<br> к шинопроводу.'),
        ('Зафиксировать', 'Установите до щелчка.<br> Убедитесь, что механический фиксатор удерживает светильник.'),
        ('Переместить', 'Используйте кнопки фиксатора, чтобы снять светильник и установить его в другом месте.'),
    ]
    for i, (title, text) in enumerate(steps, 1):
        section += '<li class="installation-step"><button type="button" class="installation-step-image" data-install-preview="'+title+'" aria-label="Увеличить схему: '+title+'" aria-haspopup="dialog" aria-controls="schemeDialog">'+image_fn(settings['s06']['image'+str(i)], 'installation-step-diagram', title+' светильник в магнитном шинопроводе')+'</button><div class="installation-step-copy"><div class="installation-step-heading"><span class="installation-step-number" aria-hidden="true">0'+str(i)+'</span><h3>'+title+'</h3></div><p>'+text+'</p></div></li>'
    return section+'''</ol></div><p class="installation-safety">Устанавливайте и перемещайте светильники при отключённом питании. Следуйте инструкции к выбранной модели.</p></div></section>\n'''
