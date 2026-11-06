"""Approved local first-screen copy and native vector benefit icons."""
import html
HERO_COPY = 'Общий и акцентный свет для дома и бизнеса. Два исполнения шинопровода — Про и Эко — с общей линейкой светильников. Выбирайте способ монтажа и форму световой линии под свой интерьер.'
BENEFITS = [
 ('Контроль качества', 'Проверка на производстве.', '<circle cx="12" cy="12" r="9"></circle><path d="m8 12 3 3 5-6"></path>'),
 ('Гарантия 3 года', 'На оборудование «Победа».', '<path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6z"></path><path d="m8 12 3 3 5-6"></path>'),
 ('Документы для проекта', 'Инструкции и спецификации.', '<path d="M14 3H5v18h14V8zM14 3v5h5M8 12h8M8 16h6"></path>'),
 ('Посмотрите вживую', 'Шоурумы в Москве и Санкт-Петербурге.', '<path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"></path><circle cx="12" cy="10" r="2.5"></circle>'),
 ('В наличии в России', 'Светильники и компоненты системы.', '<path d="m3 7 9-4 9 4v10l-9 4-9-4Zm0 0 9 4 9-4M12 11v10M7.5 5l9 4"></path>'),
]
TITLE_LINES = {
 'Контроль качества': ('Контроль', 'качества'),
 'Гарантия 3 года': ('Гарантия', '3 года'),
 'Документы для проекта': ('Документы', 'для проекта'),
 'Посмотрите вживую': ('Посмотрите', 'вживую'),
 'В наличии в России': ('В наличии', 'в России'),
}
def benefits_markup():
 return '<div class="wrap facts" aria-label="Преимущества покупки">'+''.join('<div class="fact"><svg class="fact-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">'+icon+'</svg><div><b>'+'<br> '.join(html.escape(line) for line in TITLE_LINES[title])+'</b><span>'+html.escape(copy)+'</span></div></div>' for title,copy,icon in BENEFITS)+'</div>'
