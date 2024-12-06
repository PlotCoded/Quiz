import json

with open("Storage.json","r") as file:
	content = file.read()
	content = json.loads(content)

def write(content):
	#Rewriting/Storing any changes made(to the "content" dictionary) into the JSON file
	with open("Storage.json","w") as file:
		content = json.dumps(content, indent=4)
		file.write(content)

def getSubjectList():
	return list(content.keys())

def getNumberOfQuestions(subject):
	return list(content[subject][2]["questions"].keys())[-1].split(" ")[1]

def getTime(subject):
	return content[subject][0]["details"]["time"]

def getMarks(subject):
	return content[subject][0]["details"]["marks"]

def getQuestions(subject, action="questions"):
	if action == "questions":
		return list(content[subject][2]["questions"].values())
	elif action == "length":
		return len(list(content[subject][2]["questions"].values()))
	else:
		raise Exception("Actions can only be 'questions' or 'length'")

def getQuestionKeys(subject):
	return list(content[subject][2]["questions"].keys())

def getOptionType(subject):
	return list(content[subject][1]["option_type"].values())

def getOptions(subject):
	return list(content[subject][3]["options"].values())

def getAnswers(subject):
	return list(content[subject][4]["answers"].values())

def addSubject(subject, details={}, option_type={}, questions={}, options={}, answers={}, 
	content=content):
	content.update({subject: [{"details":details}, {"option_type":option_type},
		{"questions":questions},{"options":options},{"answers":answers}]})
	print(content)

	write(content)

	#Note: "addSubject" function can be used to change sub parts, i.e, details, option type,
	#questions, etc but it is not recommended.

def addDetails(subject, details={}, content=content):
	content[subject][0]["details"].update(details)

	write(content)

def addOptionType(subject, option_type={}, content=content):		
	content[subject][1]["option_type"].update(option_type)

	write(content)

def addQuestions(subject, questions, content=content):		
	content[subject][2]["questions"].update(questions)

	write(content)

def addOptions(subject, options={}, content=content):		
	content[subject][3]["options"].update(options)

	write(content)

def addAnswers(subject, answers={}, content=content):		
	content[subject][4]["answers"].update(answers)

	with open("Storage.json","w") as file:
		content = json.dumps(content, indent=4)
		file.write(content)

def addBefore(subject, question_number, option_type={"Question 1":"Options"}, question={}, option={}, answer={}, content=content):
	#Options type
	keys = list(content[subject][1]["option_type"].keys())
	options_type = list(content[subject][1]["option_type"].values())

	keys = keys[question_number-1::]
	options_type =  options_type[question_number-1::]

	for _ in keys:
		del content[subject][1]["option_type"][_]

	content[subject][1]["option_type"].update(option_type)

	i = 0
	for _ in range(question_number +1, question_number + len(options_type) + 1):
		content[subject][1]["option_type"].update({f"Question {_}":f"{options_type[i]}"})
		i+=1

	#Questions
	keys = list(content[subject][2]["questions"].keys())
	questions = list(content[subject][2]["questions"].values())

	keys = keys[question_number-1::]
	questions =  questions[question_number-1::]

	for _ in keys:
		del content[subject][2]["questions"][_]

	content[subject][2]["questions"].update(question)
	
	i = 0
	for _ in range(question_number +1, question_number + len(questions) + 1):
		content[subject][2]["questions"].update({f"Question {_}":f"{questions[i]}"})
		i+=1

	#options
	if option != {}:
		keys = list(content[subject][3]["options"].keys())
		options = list(content[subject][3]["options"].values())

		keys = keys[question_number-1::]
		options =  options[question_number-1::]

		for _ in keys:
			del content[subject][3]["options"][_]

		content[subject][3]["options"].update(option)
		
		i = 0
		for _ in range(question_number +1, question_number + len(options) + 1):
			content[subject][3]["options"].update({f"Question {_}":options[i]})
			i+=1

	#Answers
	keys = list(content[subject][4]["answers"].keys())
	answers = list(content[subject][4]["answers"].values())

	keys = keys[question_number-1::]
	answers =  answers[question_number-1::]

	for _ in keys:
		del content[subject][4]["answers"][_]

	content[subject][4]["answers"].update(answer)
	
	i = 0
	for _ in range(question_number +1, question_number + len(answers) + 1):
		content[subject][4]["answers"].update({f"Question {_}":answers[i]})
		i+=1

	write(content)

def addAfter(subject, question_number, option_type, question, option, answer,content=content):
	#Option type
	keys = list(content[subject][1]["option_type"].keys())
	options_type = list(content[subject][1]["option_type"].values())

	keys = keys[question_number::]
	options_type = options_type[question_number::]

	for _ in keys:
		del content[subject][1]["option_type"][_]

	content[subject][1]["option_type"].update(option_type)

	i = 0
	for _ in range(question_number + 2, question_number + len(options_type) + 2):
		content[subject][1]["option_type"].update({f"Question {_}":options_type[i]})
		i+=1

	#Questions
	keys = list(content[subject][2]["questions"].keys())
	questions = list(content[subject][2]["questions"].values())

	keys = keys[question_number::]
	questions = questions[question_number::]

	for _ in keys:
		del content[subject][2]["questions"][_]

	content[subject][2]["questions"].update(question)

	i = 0
	for _ in range(question_number + 2, question_number + len(questions) + 2):
		content[subject][2]["questions"].update({f"Question {_}":questions[i]})
		i+=1

	#Options
	if option != {}:
		keys = list(content[subject][3]["options"].keys())
		options = list(content[subject][3]["options"].values())

		keys = keys[question_number::]
		options = options[question_number::]

		for _ in keys:
			del content[subject][3]["options"][_]

		content[subject][3]["options"].update(option)

		i = 0
		for _ in range(question_number + 2, question_number + len(options) + 2):
			content[subject][3]["options"].update({f"Question {_}":options[i]})
			i+=1

	#Answers
	keys = list(content[subject][4]["answers"].keys())
	answers = list(content[subject][4]["answers"].values())

	keys = keys[question_number::]
	answers = answers[question_number::]

	for _ in keys:
		del content[subject][4]["answers"][_]

	content[subject][4]["answers"].update(answer)

	i = 0
	for _ in range(question_number + 2, question_number + len(answers) + 2):
		content[subject][4]["answers"].update({f"Question {_}":answers[i]})
		i+=1
	
	write(content)

def changeSubjectName(subject, new_subject, content=content):
	val = content[subject]
	content.update({new_subject:val})
	content[new_subject][0]["details"]["name"] = new_subject

	del content[subject]

	write(content)

def changeSubjectDetails(subject, time, marks, content=content):		
	content[subject][0]["details"].update({"time":time})
	content[subject][0]["details"].update({"marks":marks})

	write(content)

def changeQuestion(subject, question, content=content):
	content[subject][2]["questions"][list(question.keys())[0]] = list(question.values())[0];

	write(content)

def changeOptionType(subject, option_type, content=content):
	content[subject][1]["option_type"][list(option_type.keys())[0]] = list(option_type.values())[0];

	write(content)

def changeOption(subject, option, content=content):		
	content[subject][3]["options"][list(option.keys())[0]] = list(option.values())[0];

	write(content)

def changeAnswer(subject, answer, content=content):		
	content[subject][4]["answers"][list(answer.keys())[0]] = list(answer.values())[0];

	write(content)

def deleteSubject(subject):
	del content[subject]

	write(content)

#deleteQuestion doesn't quite work
def deleteQuestion(subject, question_number, content=content):
	#Option type
	keys = list(content[subject][1]["option_type"].keys())
	options_type = list(content[subject][1]["option_type"].values())

	if len(options_type) != question_number:
		keys = keys[question_number::]
		options_type = options_type[question_number::]

		for _ in keys:
			del content[subject][1]["option_type"][_]

	elif len(options_type) == question_number:
		keys = keys[question_number-1::]
		options_type = options_type[question_number-1::]

		for _ in keys:
			del content[subject][1]["option_type"][_]

			options_type = options_type[question_number::]
		
	if len(options_type) != question_number:
		i = 0	
		for _ in range(question_number, question_number + len(options_type)):
			content[subject][1]["option_type"].update({f"Question {_}":options_type[i]})
			i+=1

	#Question
	keys = list(content[subject][2]["questions"].keys())
	questions = list(content[subject][2]["questions"].values())

	if len(questions) != question_number:
		keys = keys[question_number::]
		questions = questions[question_number::]

		for _ in keys:
			del content[subject][2]["questions"][_]

	elif len(questions) == question_number:
		keys = keys[question_number-1::]
		questions = questions[question_number-1::]

		for _ in keys:
			del content[subject][2]["questions"][_]

			questions = questions[question_number::]
		
	if len(questions) != question_number:
		i = 0	
		for _ in range(question_number, question_number + len(questions)):
			content[subject][2]["questions"].update({f"Question {_}":questions[i]})
			i+=1

	#Options
	keys = list(content[subject][3]["options"].keys())
	options = list(content[subject][3]["options"].values())

	if len(options) != question_number:
		keys = keys[question_number::]
		options = options[question_number::]

		for _ in keys:
			del content[subject][3]["options"][_]

	elif len(options) == question_number:
		keys = keys[question_number-1::]
		options = options[question_number-1::]

		for _ in keys:
			del content[subject][3]["options"][_]

			options = options[question_number::]
		
	if len(options) != question_number:
		i = 0	
		for _ in range(question_number, question_number + len(options)):
			content[subject][3]["options"].update({f"Question {_}":options[i]})
			i+=1

	#Answers
	keys = list(content[subject][4]["answers"].keys())
	answers = list(content[subject][4]["answers"].values())

	if len(answers) != question_number:
		keys = keys[question_number::]
		answers = answers[question_number::]

		for _ in keys:
			del content[subject][4]["answers"][_]

	elif len(answers) == question_number:
		keys = keys[question_number-1::]
		answers = answers[question_number-1::]

		for _ in keys:
			del content[subject][4]["answers"][_]

			answers = answers[question_number::]
		
	if len(answers) != question_number:
		i = 0	
		for _ in range(question_number, question_number + len(answers)):
			content[subject][4]["answers"].update({f"Question {_}":answers[i]})
			i+=1

	write(content)

#Testing
if __name__ == "__main__":
	sub = "Maths"
	addSubject(sub, 
		details={"name":sub,
		"marks":100,
		"time":"00:01:00"},
		option_type={"Question 1":"Options"}, 
		questions={"Question 1":"What is pi?"}, 
		options={"Question 1":[1.15,1,3.1415,3.5]}, 
		answers={"Question 1":3.1451}
		)
	print(getMarks(sub), getTime(sub))
	addDetails(sub,
		details={"name":sub,
		"marks":50,
		"time":"00:02:30"})
	print(getMarks(sub), getTime(sub))
	addOptionType(sub, 
		option_type={"Question 2":"Options"})
	print(getOptionType(sub))
	addQuestions(sub, 
		questions={"Question 2":"What is the value of b when a = 0 and b = a + 1?"})
	print(getQuestions(sub))
	addOptions(sub, 
		options={"Question 2":[0,1,2,3]})
	print(getOptions(sub))
	addAnswers(sub, 
		answers={"Question 2":1})
	print(getAnswers(sub))
	addBefore(sub, 
		1,
		option_type={"Question 1":"Options"}, 
		question={"Question 1":"What is log 2(base 2)?"}, 
		option={"Question 1":[-1,1,0,2]}, 
		answer={"Question 1":1}
		)
	addAfter(sub,
		1,
		option_type={"Question 2":"Options"}, 
		question={"Question 2":"What is log 2(base 4)?"}, 
		option={"Question 2":[0,2,1,1.5]}, 
		answer={"Question 2":2})
	# deleteSubject(sub)