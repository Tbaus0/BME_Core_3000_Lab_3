This script is used to make a custom filter for a persons hearing so that all tones played from headphones come
out at an equal volume. To do this an equal loudness filter is created based on 10 trial inputs from the user.
from the trial inputs a filter is made so that when convolved with any chord or multiple different octaves 
they will all play at equal loudness. This filter can be used on everyday speech as well. The script will give you 
three figures, one depicting the steps toward the filter and relative loudness, one showing the filter in both time domain
and frequancy domain, and one showing the difference bewteen the filtered and non-filtered speech test.
