set -e
python3 scripts/make_suffix_array.py $1
cargo run self-similar --data-file $1 --length-threshold $3 --cache-dir tmp/cache --num-threads $4
cargo run collect --data-file $1 --cache-dir tmp/cache --length-threshold $3 > tmp/cache/drop_tokens_file
python3 scripts/finish_single_file.py $1 tmp/cache/drop_tokens_file $2 --full-line
rm -r tmp/cache
