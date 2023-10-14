#!/bin/bash

folder="ProgramToSend"
chunksize=100


if ! command -v qrencode &>/dev/null; then
  # install qrencode if it is not installed
  sudo apt-get update
  sudo apt-get install -y qrencode
fi

# loop over all files in the folder and its subdirectories
for each_file in "$folder"/* "$folder"/*/*; do
  # check if the current item is a file
  if [[ -f "$each_file" ]]; then
    # split the file into 100-character chunks and store them in an array
    chunks=()
    while IFS= read -r -n $chunksize chunk; do
      chunks+=("$chunk")
    done < "$each_file"
    num_chunks=${#chunks[@]}

    # generate a QR code from each chunk and wait for user input

    for i in "${!chunks[@]}"; do
      clear
      echo "Processing file: $each_file"
      echo "number: $((i+1)) of $num_chunks:"
      echo "${chunks[i]}" | qrencode -t ansiutf8
      # wait for user input of "s" to skip file or any other key to continue
      while true; do
        echo "Press 's' to skip file, any other key to continue"
        read -n1 input
        if [[ $input == "s" ]]; then
          break 2
        elif [[ -n $input ]]; then
          break
        fi
        sleep 1
      done
    done
  fi
done