" Copyright (c) 2018, 2020, Xianguang Zhou <xianguang.zhou@outlook.com>. All rights reserved.
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

function! gui#Decorated(setting) abort
  call rpcnotify(g:gui_channel, 'Gui', 'Decorated', a:setting)
endfunction

function! gui#Colors(foreground, background, palette) abort
  call rpcnotify(g:gui_channel, 'Gui', 'Colors', a:foreground, a:background, a:palette)
endfunction

function! gui#Palette(palette) abort
  call gui#Colors('', '', a:palette)
endfunction
