if !has("python3")
  echo "vim has to be compiled with +python3 to run this"
  finish
endif

if exists('g:sample_python_plugin_loaded')
    finish
endif


let s:plugin_root_dir = fnamemodify(resolve(expand('<sfile>:p')), ':h')

python3 << EOF
import sys
from os.path import normpath, join
import vim
plugin_root_dir = vim.eval('s:plugin_root_dir')
python_root_dir = normpath(join(plugin_root_dir, '..', 'python'))
sys.path.insert(0, python_root_dir)
import plugin
EOF

let g:vim_codex_conf =
      \ get( g:, 'vim_codex_conf', '' )

imap <C-e> <C-\><C-O>:python3 plugin.create_completion()<CR><C-\><C-O>me
imap <C-l> <C-\><C-O>:python3 plugin.create_completion(param={"stop":"\n"})<CR><C-\><C-O>me

let g:sample_python_plugin_loaded = 1
