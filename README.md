# denite-ctags

ctags source for denite.nvim

## Configuration

```vim
augroup denite_settings
  autocmd!
  autocmd BufEnter *
        \   if empty(&buftype)
        \|      nnoremap <silent><buffer> <C-]> :<C-u>Denite ctags:`expand('<cword>')`<CR>
        \|  endif
augroup END
```
