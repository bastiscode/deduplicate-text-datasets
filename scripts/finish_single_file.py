# Copyright 2022 Google LLC
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("original", type=str)
    parser.add_argument("remove_file", type=str)
    parser.add_argument("deduped", type=str)
    parser.add_argument("--full-line", action="store_true")
    args = parser.parse_args()

    remove = []
    fin = open(args.remove_file)
    for line in fin:
        if 'out' in line:
            break
    for line in fin:
        remove.append(list(map(int, line.split())))
    remove = remove[::-1]
    if len(remove) == 0:
        print("no duplicates to remove")
        exit()

    ds = open(args.original, "rb")
    new_ds = open(args.deduped, "wb")

    if not args.full_line:
        start = 0
        while len(remove) > 0:
            a, b = remove.pop()
            new_ds.write(ds.read(a-start))
            ds.seek(b)
            start = b
        new_ds.write(ds.read())

    else:
        bytes_read = 0
        a, b = remove.pop()
        for line in ds:
            bytes_read += len(line)

            # check whether this line should be written
            if a == bytes_read - 1:
                a += 1
                b = max(a + 1, b)

            if a >= bytes_read and b > bytes_read:
                new_ds.write(line)

            # cycle through all parts that are
            # completely contained in this line
            while b <= bytes_read:
                if len(remove) == 0:
                    # if no more chunks to remove just set
                    # the next to maxsize, such that
                    # all remaining lines are still written
                    a, b = sys.maxsize, sys.maxsize
                else:
                    a, b = remove.pop()

    new_ds.close()
    ds.close()
