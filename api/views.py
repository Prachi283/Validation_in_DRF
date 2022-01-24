from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .models import Employee
from .serializers import EmpSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

@method_decorator(csrf_exempt,name='dispatch')
class EmpAPI(View):
	def get(self,request,*args,**kwargs):
		json_data=request.body
		stream=io.BytesIO(json_data)
		pythondata=JSONParser().parse(stream)
		id=pythondata.get('id',None)
		if id is not None:
			em = Employee.objects.get(id=id)
			serializer= EmpSerializer(em)
			json_data=JSONRenderer().render(serializer.data)
			return HttpResponse(json_data,content_type='application/json')

		em = Employee.objects.all()
		serializer=EmpSerializer(em, many=True)
		json_data=JSONRenderer().render(serializer.data)
		return HttpResponse(json_data,content_type='application/json')

	def post(self,request,*args,**kwargs):
		json_data=request.body
		stream = io.BytesIO(json_data)
		pythondata=JSONParser().parse(stream)
		serializer=EmpSerializer(data=pythondata)
		if serializer.is_valid():
			serializer.save()
			res= {'msg':'Data is Created'}
			json_data=JSONRenderer().render(res)
			return HttpResponse(json_data,content_type='application/json')
		json_data=JSONRenderer().render(serializer.errors)
		return HttpResponse(json_data,content_type='application/json')

		
	def put(self,request,*args,**kwargs):
		json_data=request.body
		stream=io.BytesIO(json_data)
		pythondata=JSONParser().parse(stream)
		id=pythondata.get('id')
		em=Employee.objects.get(id=id)
		serializer=EmpSerializer(em,data=pythondata)
		if serializer.is_valid():
			serializer.save()
			res={'msg':'Data is Updated'}
			json_data=JSONRenderer().render(res)
			return HttpResponse(json_data,content_type='application/json')
		json_data=JSONRenderer().render(serializer.errors)
		return HttpResponse(json_data,content_type='application/json')

	def delete(self,request,*args,**kwargs):
		json_data=request.body
		stream=io.BytesIO(json_data)
		pythondata=JSONParser().parse(stream)
		id= pythondata.get('id')
		em=Employee.objects.get(id=id)
		em.delete()
		res={'msg':'Data is Deleted'}
		json_data=JSONRenderer().render(res)
		return HttpResponse(json_data,content_type='application/json')







