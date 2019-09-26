" Copyright (C) 2018, 2019, Xianguang Zhou <xianguang.zhou@outlook.com>
" license: AGPL-3.0

" Set GUI font.
function! gui#Font(font_str) abort
  call rpcnotify(g:gui_channel, 'Gui', 'Font', a:font_str)
endfunction

function! gui#WinPos(x, y) abort
  call rpcnotify(g:gui_channel, 'Gui', 'WinPos', a:x, a:y)
endfunction

function! gui#Opacity(opacity) abort
  call rpcnotify(g:gui_channel, 'Gui', 'Opacity', a:opacity)
endfunction

function! gui#Image(path, opacity) abort
  call rpcnotify(g:gui_channel, 'Gui', 'Image', a:path, a:opacity)
endfunction

function! gui#Maximize(maximize) abort
  call rpcnotify(g:gui_channel, 'Gui', 'Maximize', a:maximize)
endfunction

