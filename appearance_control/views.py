import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt


def find_intersections(intervals1, intervals2):
    intersections = []
    len1, len2 = len(intervals1), len(intervals2)
    i1, i2 = 0, 0
    while i1 < len1 and i2 < len2:
        start1, end1 = intervals1[i1]
        start2, end2 = intervals2[i2]
        if start1 > end2:
            i2 += 1
            continue
        if start2 > end1:
            i1 += 1
            continue
        inter_start = max(start1, start2)
        inter_end = min(end1, end2)
        intersections.append((inter_start, inter_end))
        if end1 < end2:
            i1 += 1
        else:
            i2 += 1
    return intersections


def get_clean_intervals(orig):
    i = 2
    inters = []
    earliest_i, latest_i = 0, 1
    while i < len(orig):
        if orig[latest_i] >= orig[i]:
            if orig[latest_i] < orig[i + 1]:
                latest_i = i + 1
        else:
            inters.append((orig[earliest_i], orig[latest_i]))
            earliest_i, latest_i = i, i + 1
        i += 2
    inters.append((orig[earliest_i], orig[latest_i]))
    return inters

@csrf_exempt
def index(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        tutor_on_lesson = find_intersections(get_clean_intervals(data['lesson']), get_clean_intervals(data['tutor']))
        final_intersect = find_intersections(tutor_on_lesson, get_clean_intervals(data['pupil']))
        result = 0
        for inter in final_intersect:
            result += inter[1] - inter[0]
        return HttpResponse(result)


