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

let s:buf_text_changed = 0
function s:GuiBufTextChangedI() abort
  if !s:buf_text_changed
    let s:buf_text_changed = 1
    call rpcnotify(g:gui_channel, 'Gui', 'Changed', 1)
  endif
endfunction
autocmd TextChangedI * call s:GuiBufTextChangedI()
function s:GuiBufWrited() abort
  if s:buf_text_changed
    let s:buf_text_changed = 0
    call rpcnotify(g:gui_channel, 'Gui', 'Changed', 0)
  endif
endfunction
autocmd BufWritePost * call s:GuiBufWrited()
function s:GuiBufTextChanged() abort
  let buf_changed = getbufinfo('%')[0]['changed']
  if buf_changed
    call s:GuiBufTextChangedI()
  else
    call s:GuiBufWrited()
  endif
endfunction
autocmd TextChanged * call s:GuiBufTextChanged()

let s:last_buf_path = ''
function s:GuiBufEntered() abort
  let buf_name = bufname('%')
  let buf_info = getbufinfo('%')[0]
  let buf_changed = buf_info['changed']
  if buf_name == ''
    let buf_path = ''
  else
    let buf_path = fnamemodify(buf_info['name'], ':~')
  endif
  if s:last_buf_path != buf_path || s:buf_text_changed != buf_changed
    let s:last_buf_path = buf_path
    let s:buf_text_changed = buf_changed
    call rpcnotify(g:gui_channel, 'Gui', 'Buffer', buf_path, buf_changed)
  endif
endfunction
autocmd BufEnter,WinEnter,DirChanged,TermOpen * call s:GuiBufEntered()
if v:vim_did_enter
  call s:GuiBufEntered()
else
  autocmd VimEnter * call s:GuiBufEntered()
endif

function s:GuiVimEnter() abort
  call rpcnotify(g:gui_channel, 'Gui', 'VimEnter')
endfunction
if v:vim_did_enter
  call s:GuiVimEnter()
else
  autocmd VimEnter * call s:GuiVimEnter()
endif

