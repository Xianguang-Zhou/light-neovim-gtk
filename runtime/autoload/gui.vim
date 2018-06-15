" Copyright (C) 2018 Xianguang Zhou <xianguang.zhou@outlook.com>
" license: AGPL-3.0

" Set GUI font.
function! gui#Font(font_str) abort
  call rpcnotify(g:gui_channel, 'Gui', 'Font', a:font_str)
endfunction

