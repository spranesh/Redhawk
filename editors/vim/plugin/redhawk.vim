" NOTE: Redhawk must be installed in your path.
" Redhawk can be installed via PyPi: 
"   $ pip install redhawk
"
" The project hompage is here:http://pypi.python.org/pypi/redhawk
" Currently, only redhawk query is supported.
" EXAMPLE USAGE:
"
" 1. Query for '**/DefineFunction' in each FILE:
"   Redhawk query '**/DefineFunction' [FILE]
"
" 2. Query parallely for '**/DefineFunction' in each FILE:
"   Redhawk query '**/DefineFunction' [FILE] -p
"
" 3. Query all buffers for '**/DefineFunction':
"   RedhawkBuf query '**/DefineFunction'
"
" 4. Query all args for '**/DefineFunction':
"   RedhawkArgs query '**/DefineFunction'
"
" 5. Replace all results of '**/DefineFunction'
"   Redhawk replace '**/DefineFunction' [FILE] -p
"
" 6. Replace all results for '**/DefineFunction' in buffers:
"   RedhawkBuf replace '**/DefineFunction'
"
" 7. Replace all results for '**/DefineFunction' in args:
"   RedhawkArgs replace '**/DefineFunction'

if exists("g:loaded_redhawk")
  finish
endif
let g:loaded_redhawk = 1

if !exists("g:redhawk_program")
  let g:redhawk_program="redhawk"
endif

if !exists("g:redhawk_format")
  let g:redhawk_format="%f:%l:%m"
endif

if !exists("g:redhawk_args")
  let g:redhawk_args = ""
endif

if !exists("g:redhawk_open_resultlist")
  let g:redhawk_open_resultlist=1
endif

if &isfname =~ '['
    let s:redhawk_bufname = '[Redhawk\ Replace]'
else
    let s:redhawk_bufname = '\[Redhawk\ Replace\]'
endif

if v:version < 700
    finish
endif

" Line continuation saved and used here
let s:cpo_save = &cpo
set cpo&vim

function! s:Warn(msg)
    echohl WarningMsg
    echomsg a:msg
    echohl None
endfunction

function! s:GetFileList(from)
  " GetFileList
  " from can be one of
  "   * args 
  "   * buf
  "   * "" <- empty string
  let filenames = ""
  if a:from == ""
    return ""
  endif

  " Set filelnames to the list of arguments
  if a:from == "arg"
    let arg_count = argc()

    if arg_count == 0
        call s:Warn('Error: Argument list is empty')
        return
    endif

    let filenames = ""
    for i in range(0, arg_count - 1)
        let filenames .= " " . argv(i)
    endfor
    return filenames
  endif

  " Set filenames to the list of buffers
  if a:from == "buf"
    let filenames = ""
    for i in range(1, bufnr('$'))
        let bname = bufname(i)
        if bufexists(i) && buflisted(i) && filereadable(bname) &&
                    \ getbufvar(i, '&buftype') == ''
            let filenames .= ' ' . bufname(i)
        endif
    endfor
    return filenames
  endif
endfunction

let s:save_qf_list = {}

function! s:Merge()
    if empty(s:save_qf_list)
        return
    endif

    let change_all = v:cmdbang

    let changeset = {}

    " Parse the replace buffer contents and get a List of changed lines
    let lines = getbufline('%', 1, '$')
    for l in lines
        if l !~ '[^:]\+:\d\+:.*'
            continue
        endif

        let match_l = matchlist(l, '\([^:]\+\):\(\d\+\):\(.*\)')
        let fname = match_l[1]
        let lnum = match_l[2]
        let text = match_l[3]

        let key = fname . ':' . lnum
        if s:save_qf_list[key].text == text
            " This line is not changed
            continue
        endif

        let fname = s:save_qf_list[key].fname
        if !has_key(changeset, fname)
            let changeset[fname] = {}
        endif

        let changeset[fname][lnum] = text
    endfor

    if empty(changeset)
        " The replace buffer is not changed by the user
        call s:Warn('Error: No changes in the replace buffer')
        return
    endif

    " Make the changes made by the user to the buffers
    for f in keys(changeset)
        let f_l = changeset[f]
        if !filereadable(f)
            continue
        endif
        silent! exe 'hide edit ' . f

        let change_buf_all = 0   " Accept all the changes in this buffer

        for lnum in keys(f_l)
            exe lnum

            let cur_ltext = getline(lnum)
            let new_ltext = f_l[lnum]

            let s_idx =0
            while cur_ltext[s_idx] == new_ltext[s_idx]
                let s_idx += 1
            endwhile

            let e_idx1 = strlen(cur_ltext) - 1
            let e_idx2 = strlen(new_ltext) - 1
            while e_idx1 >= 0 && cur_ltext[e_idx1] == new_ltext[e_idx2]
                let e_idx1 -= 1
                let e_idx2 -= 1
            endwhile

            let e_idx1 += 2

            if (s_idx + 1) == e_idx1 
                " If there is nothing to highlight, then highlight the
                " last character
                let e_idx1 += 1
            endif

            let hl_pat = '/\%'.lnum.'l\%>'.s_idx.'v.*\%<'.e_idx1.'v/'
            exe '2match RedhawkText ' . hl_pat
            redraw!

            try
                let change_line = 0

                if !change_all && !change_buf_all
                    let new_text_frag = strpart(new_ltext, s_idx,
                                \ e_idx2 - s_idx + 1)

                    echo "Replace with '" . new_text_frag . "' (y/n/a/b/q)?"
                    let ans = 'x'
                    while ans !~? '[ynab]'
                        let ans = nr2char(getchar())
                        if ans == 'q' || ans == "\<Esc>"      " Quit
                            return
                        endif
                    endwhile
                    if ans == 'a'       " Accept all
                        let change_all = 1
                    endif
                    if ans == 'b'       " Accept changes in the current buffer
                        let change_buf_all = 1
                    endif
                    if ans == 'y'       " Yes
                        let change_line = 1
                    endif
                endif

                if change_all || change_buf_all || change_line
                    call setline(lnum, f_l[lnum])
                endif
            finally
                2match none
            endtry
        endfor
    endfor
endfunction

function! s:EditQuickFixList()
    let qf = getqflist()
    if empty(qf)
        call s:Warn('Error: Quickfix list is empty')
        return
    endif

    let new_qf = {}

    " Populate the buffer with the current quickfix list
    let lines = []
    for l in qf
        if l.valid && l.lnum > 0 && l.bufnr > 0
            let fname = fnamemodify(bufname(l.bufnr), ':.')
            let buf_text = fname . ':' . l.lnum . ':' . l.text
            let k = fname . ':' . l.lnum
            let new_qf[k] = {}
            let new_qf[k].fname = fnamemodify(bufname(l.bufnr), ':p')
            let new_qf[k].text = l.text
        else
            let buf_text = l.text
        endif

        call add(lines, buf_text)
    endfor

    if empty(lines)
        " No valid matching lines
        return
    endif

    let w = bufwinnr(s:redhawk_bufname)
    if w == -1
        " Create a new window
        silent! exe 'new ' . s:redhawk_bufname
    else
        exe w . 'wincmd w'

        " Discard the contents of the buffer
        %d _
    endif

    call append(0, '#')
    call append(1, '# Modify the contents of this buffer and then')
    call append(2, '# use the ":RedhawkMerge" command to merge the changes.')
    call append(3, '#')
    call append(4, lines)

    call cursor(5, 1)
    setlocal buftype=nofile
    setlocal bufhidden=wipe
    setlocal nomodified

    command! -buffer -nargs=0 -bang RedhawkMerge call s:Merge()

    let s:save_qf_list = new_qf
endfunction


function! s:Query(command, arguments)
  redraw!
  echo "Searching ..."
  " Query args
  let arguments = join(a:arguments, " ")
  if empty(arguments)
    s:Warn("No arguments to Redhawk")
  endif

  let backup_grepprg=&grepprg
  let backup_grepformat=&grepformat
  let backup_shellpipe=&shellpipe

  try
    let &grepprg = g:redhawk_program
    let &grepformat = g:redhawk_format
    let &shellpipe = ">"
    execute a:command . " query " . arguments . g:redhawk_args
  finally
    let &grepprg = backup_grepprg
    let &grepformat = backup_grepformat
    let &shellpipe = backup_shellpipe
  endtry

endfunction

function! s:OpenQuickFix()
  if g:redhawk_open_resultlist
    botright copen
  endif
endfunction

highlight RedhawkText term=reverse cterm=reverse gui=reverse

function! s:Redhawk(command, add_from, ...)
  " Call Query with command, and arguments after adding files from add_from,
  " and removing the word query from the start of arguments if present.

  let filenames = s:GetFileList(a:add_from)

  let arguments = a:000 + [filenames]

  echo arguments

  if arguments[0] == "query"
    call s:Query(a:command, arguments[1:])
    call s:OpenQuickFix()

  elseif arguments[0] == "replace"
    call s:Query(a:command, arguments[1:])
    call s:EditQuickFixList()

  else 
    call s:Query(a:command, arguments)
    call s:OpenQuickFix()
  endif
endfunction

command! -nargs=* -complete=file Redhawk         call s:Redhawk("grep!", "", <f-args>)
command! -nargs=* -complete=file RedhawkArgs     call s:Redhawk("grep!", "arg", <f-args>)
command! -nargs=* -complete=file RedhawkBuf      call s:Redhawk("grep!", "buf", <f-args>)

command! -nargs=* -complete=file RedhawkAdd      call s:Redhawk("grepadd!", "", <f-args>)
command! -nargs=* -complete=file RedhawkArgsAdd  call s:Redhawk("grepadd!", "arg", <f-args>)
command! -nargs=* -complete=file RedhawkBufAdd   call s:Redhawk("grepadd!", "buf", <f-args>)
