=============================
 Vim Codex 
=============================

.. image:: gifs/render1630418854684.gif

This is a simple plugin for Vim that will allow you to use OpenAI Codex.
To use this plugin you need to have access to OpenAI's `Codex API`_.

.. _Codex API: https://openai.com/blog/openai-codex/

This repository is a fork of `vim-codex`_ by `@tom-doerr`_.

.. _vim-codex: https://github.com/tom-doerr/vim-codex
.. _@tom-doerr: https://github.com/tom-doerr


Configuration
============

Default config file is at `~/.config/vim_codex/vim_codex.conf`.
The path could be changed with `g:vim_codex_conf`.
The API key could be supplied as::
  
  # vim_codex.conf
  {"secret_key":"XXXXXXXXX"}

Usage
=====
The plugin provides function "create_completion(params)" together with a binding::

  imap <C-e> <C-\><C-O>:python3 plugin.create_completion()<CR><Right>

Parameter `params` could be a dictionary for tuning the completion.

For example::

  create_completion({'stop':'\n'})
