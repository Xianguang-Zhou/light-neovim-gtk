" Set Gui font
function! light_neovim_gtk#font#GuiFont(font_str) abort
  call rpcnotify(g:gui_channel, 'Gui', 'Font', a:font_str)
endfunction

