# Design Notes

## Usage scenario

I am a papyrologist that wants to restore a part of a glyph based on other
glyphes inside the same list of images. I load my image list. I select the
image that I would like to work on. I choose ROI selection mode. I select the
region of interest in the image. I choose EVIDENCE selection mode. I select
the regions that are similar to my ROI from the same or other images in the
list. I select my restoration method, mainly wiener filter, I click restore,
and it saves the restored image into a designated location.

## UI Design

<table>
<thead>
  <tr>
    <th colspan="6">Wiener Filter Restoration</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td>Loaded image List</td>
    <td colspan="3">Canvas</td>
    <td colspan="2">ROI Viewer</td>
  </tr>
  <tr>
    <td rowspan="7"></td>
    <td colspan="3" rowspan="11"></td>
    <td colspan="2" rowspan="4"></td>
  </tr>
  <tr>
  </tr>
  <tr>
  </tr>
  <tr>
  </tr>
  <tr>
    <td colspan="2">Selection Radio Buttons</td>
  </tr>
  <tr>
    <td rowspan="5">Selected<br>Similar<br>Regions</td>
    <td></td>
  </tr>
  <tr>
    <td></td>
  </tr>
  <tr>
    <td>Load</td>
    <td rowspan="3">Restore<br>Options<br>Radio <br>Buttons</td>
  </tr>
  <tr>
    <td>View</td>
  </tr>
  <tr>
    <td>Save</td>
  </tr>
  <tr>
    <td>Quit</td>
    <td>Go To Region</td>
    <td>Restore</td>
  </tr>
</tbody>
</table>
