## Old Tape

### Description

We were comfortably watching our favorite cartoon in an open air cinema, when _suddenly_ the video quality dropped. It was all moshy moshed :'(
Can you try to fix the video? We really want to see this cartoon :) 

**Author: algorab**

### Solution

By looking at the video, we can see that it plays correctly, but that there are some glitches in it. After some research, we find that the video looks like it has been through some [datamoshing process](https://chalier.fr/blog/datamoshing).
Given the look of the result, we can assume that the video contains duplicated P-Frames, which gives that "glitched" effect. Therefore, it is possible to delete all the duplicated P-Frames and reexport the video.

```python
FRAME_END = bytes.fromhex('30306463')

def write_frame(output, frame):
    output.write(frame + FRAME_END)

with open("challenge.avi", 'rb') as input:
    video_data = input.read()
frames = video_data.split(FRAME_END)

video = {
    'header': frames[0],
    'frames': frames[1:]
}

output_avi = "fixed.avi"

output = open(output_avi, 'wb')

write_frame(output, video['header'])
for i in range(len(video['frames'])):
    if not video['frames'][i] in video['frames'][:i]:
        output.write(video['frames'][i] + FRAME_END)

output.close()
```
We can finally read the flag in the fixed video.

### Flag

The flag is `N0PS{4v1_f0rM4t_h4Z_n0_5eCr37_4_U_4nYM0r3}`