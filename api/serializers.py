# Validation 

from rest_framework import serializers
from .models import Employee

#  Validators 

def starts_with_p(value):
	if value[0].lower() != 'p':
		raise serializers.ValidationError('Position must be starts with letter-p')

class EmpSerializer(serializers.Serializer):
	name=serializers.CharField(max_length=200)
	email=serializers.EmailField(max_length=200)
	post=serializers.CharField(max_length=200,validators=[starts_with_p])
	emp=serializers.IntegerField()

	def create(self,validated_data):
		return Employee.objects.create(**validated_data)

	def update(self,instance,validated_data):
		print(instance.name)
		instance.name=validated_data.get('name',instance.name)
		print(instance.name)
		instance.email=validated_data.get('email',instance.email)
		instance.post=validated_data.get('post',instance.post)
		instance.emp=validated_data.get('emp_id',instance.emp)
		instance.save()
		return instance

		#  Field-Level Validation
	def validate_emp(self,value):
		if value>=500:
			raise serializers.ValidationError('Check your Employee ID again !')
		return value 

		#  Object-Level Validation

	def validate(self,data):
		nm=data.get('name')
		if nm.upper() == False:
			raise serializers.ValidationError('Name must be starts with a capital letter !')
		return data