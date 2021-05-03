#Comment
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
	import requests
	import json
	#pk_31c5bc7830ff4ea688629886d9b90cf5#

	if request.method == 'POST':
		#Action A
		ticker = request.POST['ticker'] #a
		api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=pk_31c5bc7830ff4ea688629886d9b90cf5")
		try:
			api = json.loads(api_request.content)
		except Exception as e:
			api ="Error.."
		return render(request, 'home.html', {'api': api})

	else:
		#Action a
		return render(request, 'home.html', {'ticker': "Enter a ticker symbol above"})

	

	#return render(request, 'home.html', {'api': api})

def about(request):
	return render(request, 'about.html', {})	
# Create your views here.

def add_stock(request):
	import requests
	import json

	if request.method == 'POST':
		form = StockForm(request.POST or None)

		if form.is_valid():
			form.save()
			messages.success(request, ("Stock Has Been Added"))
			return redirect('add_stock')

	else:
		ticker = Stock.objects.all()
		output = []
		for ticker_item in ticker:
			api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=pk_31c5bc7830ff4ea688629886d9b90cf5")
			try:
				api = json.loads(api_request.content)
				output.append(api)
			except Exception as e:
				api ="Error.."
		
		return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})


def delete(request, stock_id):
	item = Stock.objects.get(pk = stock_id)	
	item.delete()
	messages.success(request, ("Stock has been deleted!"))
	return redirect(delete_stock)


def delete_stock(request):
	ticker = Stock.objects.all()
	return render(request, 'delete_stock.html', {'ticker': ticker})	