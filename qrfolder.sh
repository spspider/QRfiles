#!/bin/bash

folder=$1
splitted_folder="./splitted/"
chunksize=800

if ! command -v qrencode &>/dev/null; then
  # install qrencode if it is not installed
  sudo apt-get update
  sudo apt-get install -y qrencode
fi
for each_file in "$folder"/* "$folder"/*/* "$folder"/*/*/* "$folder"/*/*/*/* "$folder"/*/*/*/*/*; do
  if [[ -f "$each_file" ]]; then
    # split the file into 100-character chunks and store them in an array
    rm -rf "$splitted_folder"
    mkdir -p "$splitted_folder"
    split --numeric-suffixes=1 --suffix-length=3 -d --additional-suffix=.chunk --verbose "$each_file" -C "$chunksize" "$splitted_folder" &>/dev/null
    num_chunks=$(ls -1 "$splitted_folder" | wc -l)
    i=0
    # generate a QR code from each chunk and wait for user input
    for each_splitted_file in "$splitted_folder"*; do
      json="{\"p\": \"$i\", \"a\": $(($num_chunks)), \"f\": \"$each_file\"}"
      ((i++))
      clear
      echo -e "$json
&&&&&&&&&&&&777777777777
$(cat $each_splitted_file)" | qrencode -t ansiutf8 -m 2 -s 2 -d 1
      while true; do
        echo "$each_file part:$i of: $num_chunks"
        read -n1 input
        if [[ $input == "s" ]]; then
          break 2
        elif [[ -n $input ]] ; then
          break
        fi
        # sleep 1
      done
    done
    rm -rf "$splitted_folder"
  fi
  # rm $each_file
done
clear
