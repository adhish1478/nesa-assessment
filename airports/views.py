from django.shortcuts import render, redirect
from .models import AirportNode
from django.http import JsonResponse
from .forms import *
from .services import *

def add_node_view(request):
    if request.method == 'POST':
        form = AddNodeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            parent = form.cleaned_data['parent']
            side = form.cleaned_data['side']
            distance = form.cleaned_data['distance']

            node = AirportNode.objects.create(name=name)

            if parent:
                if side == 'left':
                    parent.left = node
                    parent.left_distance = distance
                else:
                    parent.right = node
                    parent.right_distance = distance

                node.parent = parent

                parent.save()
                node.save()

            return redirect('add_node')
    else:
        form = AddNodeForm()

    root = AirportNode.objects.filter(parent__isnull=True).first()

    return render(request, 'airports/add_node.html', {
        'root': root,
        'form': form
    })


def distance_view(request):
    result = None
    error = None

    if request.method == 'POST':
        form = SingleNodeForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].upper()

            try:
                node = AirportNode.objects.get(name=name)
                result = distance_from_root(node)

            except AirportNode.DoesNotExist:
                error = f"Node '{name}' does not exist."

            except AirportNode.MultipleObjectsReturned:
                error = f"Multiple nodes found with name '{name}'."

    else:
        form = SingleNodeForm()

    return render(request, 'airports/distance.html', {
        'form': form,
        'result': result,
        'error': error
    })


def longest_view(request):
    root = AirportNode.objects.get(parent__isnull=True)

    distance, path = longest_from_root(root)

    return render(request, 'airports/longest.html', {
        'distance': distance,
        'path': path
    })


def shortest_view(request):
    result = None

    if request.method == 'POST':
        form = TwoNodeForm(request.POST)
        if form.is_valid():
            n1 = AirportNode.objects.get(name=form.cleaned_data['source'])
            n2 = AirportNode.objects.get(name=form.cleaned_data['destination'])
            result = distance_between(n1, n2)
    else:
        form = TwoNodeForm()

    return render(request, 'airports/shortest.html', {'form': form, 'result': result})



def build_tree(node):
    if not node:
        return None

    children = []

    if node.left:
        left_child = build_tree(node.left)
        if left_child:
            left_child["distance"] = node.left_distance
            children.append(left_child)

    if node.right:
        right_child = build_tree(node.right)
        if right_child:
            right_child["distance"] = node.right_distance
            children.append(right_child)

    return {
        "name": node.name,
        "children": children
    }

def tree_data(request):
    root = AirportNode.objects.filter(parent__isnull=True).first()
    data = build_tree(root) if root else {}
    return JsonResponse(data)