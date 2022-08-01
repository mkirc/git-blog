#!/usr/bin/env bash

set -e

TMPDIR=('tmp')
PUBDIR=('public')

getRevsForTmpPostDir() {

    local tmpPostDir="$1"
    local _posts=()
    for tmpFile in "${tmpPostDir:?}"/*; do
        filename="${tmpFile##*/}"
        if [[ "$filename" =~ ^[a-zA-Z0-9]{7}\.[a-z]+$ ]]; then
            _posts+=("$filename")
        fi
    done
    [[ "${#_posts[@]}" -ne 0 ]] && \
        { revs=("${_posts[@]}"); return; }
}

getTopNavForRev() {

    local tmpPostDir="$1"
    local post="$2"
    local short="${post%.*}"
    local elms=()
    for tmpFile in "${tmpPostDir:?}"/*; do
        filename="${tmpFile##*/}"
        if [[ "$filename" =~ "$short"_nav-top* ]]; then
            elms+=("$filename")
            fi
    done
    if [[ "${#elms[@]}" == 1 ]]; then
        { topNav="${elms[0]}"; return; }
    elif [[ "${#elms[@]}" -lt 1 ]]; then
        echo 'No nav-top of '"$post"' in '"${tmpPostDir}"', aborting.'
        exit
    elif [[ "${#elms[@]}" -gt 1 ]]; then
        echo 'More than 1 nav-top of'"$post"' in '"${tmpPostDir}"', aborting.'
        exit
    fi

}

getSideNavForTmpPostDir() {

    local tmpPostDir="$1"
    local elms=()
    for tmpFile in "${tmpPostDir:?}"/*; do
        filename="${tmpFile##*/}"
        if [[ "$filename" =~ .nav-side* ]]; then
            elms+=("$filename")
        fi
    done
    if [[ "${#elms[@]}" == 1 ]]; then
        { sideNav="${elms[0]}"; return; }
    elif [[ "${#elms[@]}" -lt 1 ]]; then
        echo 'No nav-side in '"${tmpPostDir}"', aborting.'
        exit
    elif [[ "${#elms[@]}" -gt 1 ]]; then
        echo 'More than 1 nav-side in '"${tmpPostDir}"', aborting.'
        exit
    fi
}

getPandocPath() {
    shopt -s nullglob
    local pPath=$(which pandoc)
    shopt -u nullglob
    [[ -x "$pPath" ]] && \
        { pandocPath="$pPath"; return; }
}

makePagesWithPandoc() {

    echo 'Creating page for '"$2"'...'
    local outPath=("${PUBDIR:?}"/"${1##*/}"/"${2%.*}".html)
    local inPath=("$1"/"$2")
    local sideNav=("$1"/"$3")
    local topNav=("$1"/"$4")
    # cat "$inPath"
    # echo $outPath

    "$pandocPath" --from markdown_github+smart+yaml_metadata_block+auto_identifiers "$inPath" \
        -o "$outPath" \
        --template templates/page.html \
        -V topNav="$(cat "$topNav")" \
        -V sideNav="$(cat "$sideNav")" \
        -V title="${1##*/}" \
        --toc
    
    return

}

makeIndexPageWithPandoc() {

    echo 'Creating index'
    local outPath=("${PUBDIR:?}"/index.html)
    local sideNav=("$1"/"$2")
    "$pandocPath" --from markdown_github+smart+yaml_metadata_block+auto_identifiers templates/index.md \
        -o "$outPath" \
        --template templates/index.html \
        -V sideNav="$(cat "$sideNav" | sed 's/ class="active"//g')"
    
    return
}

createPubTree() {

    shopt -s nullglob
    local tDirs=("${TMPDIR:?}"/*)
    shopt -u nullglob
    local tDirs=("${tDirs[@]%/}")
    local tDirs=("${tDirs[@]##*/}")
    if [[ "${#tDirs[@]}" -gt 0  && -d "${PUBDIR:?}" ]]; then
        for d in "${tDirs[@]}"; do
            echo 'Creating '"${PUBDIR}"'/'"$d"'...'
            # error is not caught because of pipe
            mkdir "${PUBDIR}"/"$d" 2> /dev/null || \
                { echo '...'"${PUBDIR}"'/'"$d"' already exists, skipping.'; }
        done
    fi 
    return
}

makePages() {

    local isFirst=1
    for f in "${TMPDIR:?}"/*; do
        if [[ -d "$f" ]]; then
            getRevsForTmpPostDir "$f"
            getSideNavForTmpPostDir "$f"
            for r in "${revs[@]}"; do
                getTopNavForRev "$f" "$r"
                makePagesWithPandoc "$f" "$r" "$sideNav" "$topNav" && \
                    echo 'done.'
            done
            # break # for testing reasons
            if [[ "$isFirst" -eq 1 ]]; then
                makeIndexPageWithPandoc "$f"  "$sideNav"
                isFirst=0
            fi
        fi
    done
    return

}

cleanUpTmp() {


    if [[ "$TMPDIR" =~ ^/  ]]; then
        if [[ "$TMPDIR" == '/tmp' ]]; then
            # fair enough
            true
        else
            # something bad has happened!
            exit
        fi
    elif [[ -z "$TMPDIR" ]]; then
        # just to be shure
        echo '$TMPDIR is empty, wtf?'
        exit
    fi

    for f in "${TMPDIR:?}"/*; do
        if [[ -d "$f" ]]; then
            echo 'Removing '"$f"
            rm -r "$f"
        fi
    done
    return
}

main() {

    createPubTree
    getPandocPath
    makePages
    # check probably not even necessary because of set -e
    # [[ "$?" -eq 0  ]] && \
    #     cleanUpTmp

}

main
