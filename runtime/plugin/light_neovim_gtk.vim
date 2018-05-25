" Copyright (C) 2018 Xianguang Zhou <xianguang.zhou@outlook.com>
" license: AGPL-3.0
" A Neovim plugin that implements GUI helper commands
if !has('nvim') || exists('g:GuiLoaded')
  finish
endif
let g:GuiLoaded = 1

" Set Gui font
function! GuiFont(font_str) abort
  call rpcnotify(g:gui_channel, 'Gui', 'Font', a:font_str)
endfunction

" The GuiFont command. For compatibility there is also Guifont
function s:GuiFontCommand(font_str) abort
  if a:font_str ==# ''
    if exists('g:GuiFont')
      echo g:GuiFont
    else
      echo 'No GuiFont is set'
    endif
  else
    call GuiFont(a:font_str)
  endif
endfunction
command! -nargs=? GuiFont call s:GuiFontCommand('<args>')
command! -nargs=? Guifont call s:GuiFontCommand('<args>')

let s:last_color = ''
function s:GuiColor() abort
  let current_color = synIDattr(hlID('Normal'), 'bg#', 'gui')
  if current_color != s:last_color
    let s:last_color = current_color
    call rpcnotify(g:gui_channel, 'Gui', 'Color', current_color)
  endif
endfunction
autocmd ColorScheme * call s:GuiColor()

set title
set termguicolors

function s:GuiCursor() abort
  let gui_cursor = execute('set guicursor')
  let gui_cursor = strpart(gui_cursor, stridx(gui_cursor, '=') + 1)
  let gui_cursor_parts = split(gui_cursor, ',')
  let part_index = 0
  for part in gui_cursor_parts
    let gui_cursor_parts[part_index] = part . '-blinkwait175-blinkoff150-blinkon175'
    let part_index += 1
  endfor
  let gui_cursor = join(gui_cursor_parts, ',')
  execute('set guicursor=' . gui_cursor)
endfunction
call s:GuiCursor()

