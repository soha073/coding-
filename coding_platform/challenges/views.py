from django.shortcuts import render

# Create your views here.
# challenges/views.py
from django.shortcuts import render
from .models import Problem

def show_problems(request):
    problems = Problem.objects.all()  # Django ORM query
    return render(request, 'problems.html', {'problems': problems})

# challenges/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('home')  # Redirect to a 'home' or other page after successful registration
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# challenges/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def profile(request):
    return render(request, 'profile.html')

from django.shortcuts import render
from django.http import JsonResponse
from .models import Problem, Submission, Leaderboard

def problem_list(request):
    problems = Problem.objects.all()
    return render(request, 'challenges/problem_list.html', {'problems': problems})


def leaderboard(request):
    leaderboard = Leaderboard.objects.order_by('-score')[:10]
    return render(request, 'challenges/leaderboard.html', {'leaderboard': leaderboard})

def submit_code(request):
    # Code to handle submissions goes here
    return JsonResponse({'status': 'Code submission endpoint'})

# challenges/views.py
from django.shortcuts import render, redirect
from .models import Problem, Submission, Leaderboard
from .forms import CodeSubmissionForm
from django.http import JsonResponse

def problem_detail(request, pk):
    problem = Problem.objects.get(pk=pk)
    form = CodeSubmissionForm()
    return render(request, 'challenges/problem_detail.html', {'problem': problem, 'form': form})

def submit_code(request):
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem_id = request.POST['problem_id']
            submission.status = 'P'
            submission.save()

            # Call evaluation function here (refer to previous code for evaluate_submission)
            # e.g., evaluate_submission(submission)

            return JsonResponse({'status': 'Submission received'})
    return JsonResponse({'error': 'Invalid submission'}, status=400)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Problem, Submission, Leaderboard
from .forms import CodeSubmissionForm
import subprocess

@login_required
def submit_code(request):
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.status = 'P'  # Pending
            submission.save()

            # Start the code evaluation process
            evaluate_submission(submission)

            return JsonResponse({'status': 'Submission received'})
    return JsonResponse({'error': 'Invalid submission'}, status=400)

def evaluate_submission(submission):
    # Example of how you can run the code (for Python, Java, C, etc.)
    problem = submission.problem
    test_cases = problem.test_cases
    results = []

    for test_case in test_cases:
        input_data = test_case['input']
        expected_output = test_case['expected_output']
        
        try:
            # For Python code:
            if submission.language == 'python':
                result = subprocess.run(['python3', '-c', submission.code], input=input_data, text=True, capture_output=True)
            # Add other languages like Java, C, etc.
            # You can use subprocess.run to execute Java or C code too
            result_output = result.stdout.strip()

            # Compare output with expected
            if result_output == expected_output.strip():
                results.append({'input': input_data, 'status': 'pass'})
            else:
                results.append({'input': input_data, 'status': 'fail', 'error': result.stderr})
        except Exception as e:
            results.append({'status': 'error', 'error': str(e)})

    submission.status = 'C'  # Completed after evaluation
    submission.result = {'test_cases': results, 'score': 100}  # Adjust score calculation as needed
    submission.save()

    # Update leaderboard
    update_leaderboard(submission)

def update_leaderboard(submission):
    if submission.status == 'C':  # Only update if successful
        leaderboard, created = Leaderboard.objects.get_or_create(user=submission.user)
        leaderboard.problems_solved += 1
        leaderboard.score += submission.result['score']
        leaderboard.save()

def leaderboard(request):
    leaderboard_entries = Leaderboard.objects.all().order_by('-score')
    return render(request, 'challenges/leaderboard.html', {'leaderboard_entries': leaderboard_entries})

def submission_result(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    return render(request, 'challenges/submission_result.html', {'submission': submission})

from django.shortcuts import render
from django.http import JsonResponse
from .models import Problem, Submission
from .utils import save_code_to_file, execute_code, clean_up

def handle_submission(request):
    if request.method == "POST":
        code = request.POST.get("code")
        language = request.POST.get("language")
        problem_id = request.POST.get("problem_id")
        user = request.user

        # Get the problem and determine the language extension
        problem = Problem.objects.get(id=problem_id)
        language_extension = {"python": "py", "java": "java", "cpp": "cpp"}.get(language)

        # Save the code to a temporary file
        file_path = save_code_to_file(code, language_extension)

        # Execute the code and get the output
        output = execute_code(file_path, language)

        # Clean up the temporary file
        clean_up(file_path)

        # Save the submission result to the database
        submission = Submission.objects.create(
            user=user,
            problem=problem,
            code=code,
            language=language,
            result=output
        )

        return JsonResponse({"output": output})

from .models import Leaderboard

def update_leaderboard(user, problem, result):
    # Check if the submission is correct (based on expected output)
    if result == "Expected Output":  # Replace with the actual condition
        leaderboard, created = Leaderboard.objects.get_or_create(user=user)
        leaderboard.problems_solved += 1
        leaderboard.score += 10  # You can modify this scoring logic
        leaderboard.save()

from django.shortcuts import render
from django.http import JsonResponse
from .models import Leaderboard

def leaderboard(request):
    # Get all users from the leaderboard, ordered by score (descending)
    leaderboard_data = Leaderboard.objects.all().order_by('-score')

    leaderboard_list = []
    for entry in leaderboard_data:
        leaderboard_list.append({
            'user': entry.user.username,
            'score': entry.score
        })

    return JsonResponse({'leaderboard': leaderboard_list})
