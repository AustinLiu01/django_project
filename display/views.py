from django.shortcuts import render


# Create your views here.
def display_list(request):
    context = {}
    with open('data.txt', 'r') as f:
        st = f.read()
        st = st.split('\n')
    for t in st:
        context[t.split(':')[0]] = t.split(':')[1]
    return render(request, 'display/list.html', context)
