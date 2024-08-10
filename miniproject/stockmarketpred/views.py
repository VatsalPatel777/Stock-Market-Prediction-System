from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SigninForm, SignupForm, MyForm, FeedbackForm
from .models import User, Feedback
from django.core.exceptions import ObjectDoesNotExist
from .predictorengine.Prediction import Prediction
from .predictorengine.SentimentAnalyzer import SentimentAnalyzer
from jinja2 import Template, Environment, FileSystemLoader
from django.urls import reverse


def signin(request):
    if request.method == "POST":
        form = SigninForm(request.POST)
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(email=username)
        except ObjectDoesNotExist:
            return render(
                request,
                "stockmarketpred/signin.html",
                {"error_message": f"Username {username} does not exist!"},
            )
        else:
            user = User.objects.get(username=username)
            if user.password == password:
                request.session["u_id"] = username
                return redirect("home")
            else:
                return render(
                    request,
                    "stockmarketpred/signin.html",
                    {"error_message": "Incorrect password. Please re-enter"},
                )
    else:
        form = SigninForm()
        return render(request, "stockmarketpred/signin.html", {})


def signup(request):
    flag = True
    if request.method == "POST":
        form = SignupForm(request.POST)
        psw1 = request.POST["password"]
        psw2 = request.POST["password_repeat"]

        if psw1 != psw2:
            return render(
                request,
                "stockmarketpred/signup.html",
                {"error_message": "Passwords are not matching"},
            )
        else:
            try:
                User(
                    email=request.POST["email"],
                    firstname=request.POST["fname"],
                    lastname=request.POST["lname"],
                    username=request.POST["email"],
                    password=request.POST["password"],
                ).save()

                flag = False
            except IntegrityError:
                return render(
                    request,
                    "stockmarketpred/signup.html",
                    {"error_message": "User already exists. Please sign in."},
                )
            except ValueError:
                return render(
                    request,
                    "stockmarketpred/signup.html",
                    {},
                    # {"error_message": "Invalid email address"},
                )
            else:
                if flag:
                    User(
                        email=request.POST["email"],
                        firstname=request.POST["fname"],
                        lastname=request.POST["lname"],
                        username=request.POST["username"],
                        password=request.POST["password"],
                    ).save()
                return redirect("signin")
    else:
        form = SignupForm()
        return render(request, "stockmarketpred/signup.html", {"form": form})


def signout(request):
    try:
        del request.session["u_id"]
    except KeyError:
        return redirect("index")
    else:
        return redirect("index")


def home(request):
    output_file_path = r"D:\BVM Study Material\BVM IT Sem 6\Mini Project\miniproject\stockmarketpred\templates\stockmarketpred\prediction.html"
    input_file_path = r"D:\BVM Study Material\BVM IT Sem 6\Mini Project\miniproject\stockmarketpred\myTemplates\prediction.html"

    if "u_id" not in request.session:
        return redirect("signin")
    else:
        p = Prediction()

        if request.method == "POST":
            form = MyForm(request.POST)
            if form.is_valid():
                symbol = form.cleaned_data["dropdown"]

        else:
            symbol = "RELIANCE"

        fig = p.makePredictions(symbol + ".NS")
        ma_1 = p.plotMA(symbol + ".NS", 10, "red")
        ma_2 = p.plotMA(symbol + ".NS", 20, "yellow")
        ma_3 = p.plotMA(symbol + ".NS", 50, "green")
        ma = p.plotMAinOne(symbol + ".NS")
        plotly_jinja_data = {
            "fig": fig.to_html(full_html=False),
            "ma_1": ma_1.to_html(full_html=False),
            "ma_2": ma_2.to_html(full_html=False),
            "ma_3": ma_3.to_html(full_html=False),
            "ma": ma.to_html(full_html=False),
            "var": "{% static 'stockmarketpred/images/logo2.png' %}",
        }
        request.session["fig1"] = plotly_jinja_data
        form = MyForm()
        return render(
            request,
            "stockmarketpred/home.html",
            {
                "stock_symbol": symbol,
                "form": form,
            },
        )


def predictions(request):
    output_file_path = r"D:\BVM Study Material\BVM IT Sem 6\Mini Project\miniproject\stockmarketpred\templates\stockmarketpred\prediction.html"
    input_file_path = r"D:\BVM Study Material\BVM IT Sem 6\Mini Project\miniproject\stockmarketpred\myTemplates\prediction.html"

    if "u_id" not in request.session:
        return redirect("signin")
    else:
        render_dict = request.session["fig1"]
        render_dict["homeurl"] = reverse("home")
        render_dict["marketurl"] = reverse("sentiment")
        render_dict["contacturl"] = reverse("contact")
        render_dict["predectionurl"] = reverse("predictions")
        render_dict["indexurl"] = reverse("index")
        render_dict["img_url"] = "{% static 'stockmarketpred/images/logo2.png' %}"
        render_dict["static_load"] = "{% load static %}"

        with open(output_file_path, "w", encoding="utf-8") as output_file:
            with open(input_file_path, "r", encoding="utf-8") as input_file:
                template = Template(input_file.read())
                output_file.write(template.render(request.session["fig1"]))

        return render(request, "stockmarketpred/prediction.html", context={})


def sentiment(request):
    output_file_path = r"D:\BVM Study Material\BVM IT Sem 6\Mini Project\miniproject\stockmarketpred\templates\stockmarketpred\market.html"
    input_file_path = r"D:\BVM Study Material\BVM IT Sem 6\Mini Project\miniproject\stockmarketpred\myTemplates\market.html"
    if "u_id" not in request.session:
        return redirect("signin")
    else:
        s = SentimentAnalyzer()
        plot = s.plotSentimentAnalysis()[0]
        sentiment = s.plotSentimentAnalysis()[1]

        if sentiment == "Neutral":
            text1 = """Neutral sentiment indicates a balanced view among investors, with no strong expectations for significant market 
                       movements either up or down. This can occur during periods of market consolidation, when economic indicators 
                       are mixed, or when investors are awaiting key information."""
            heading1 = "Investment Advisory:"
            text2 = """In a neutral market, a balanced investment strategy is recommended. 
                       Investors should maintain a well-diversified portfolio across various asset classes to manage risk effectively. 
                       It may also be an opportune time to review and rebalance portfolios, ensuring alignment with long-term financial goals. 
                       Investing in dividend-paying stocks can provide steady income while waiting for clearer market direction."""

        elif sentiment == "Bullish":
            text1 = """Bullish sentiment indicates a positive view among investors, with expectations for rising stock prices. 
                       This can be driven by strong economic data, positive earnings reports, or favorable market conditions.
                       Bull markets are characterized by sustained upward trends and investor optimism."""
            heading1 = "Investment Advisory:"
            text2 = """During bullish periods, investors might consider increasing their exposure to equities, particularly in sectors 
                       showing strong growth potential such as technology, consumer goods, and financial services. It's also a good time to 
                       explore high-growth stocks and index funds that mirror the overall market. However, maintaining a diversified portfolio to
                       manage risk remains crucial."""

        else:
            text1 = """Bearish sentiment reflects a negative outlook among investors, anticipating a decline in stock prices. This pessimism can 
                       result from economic downturns, poor corporate performance, political instability, or unfavorable global market trends."""
            heading1 = "Investment Advisory:"
            text2 = """In bearish times, a conservative investment approach is advisable. Investors might shift towards more defensive stocks 
                       in sectors like utilities and healthcare, or consider increasing allocations to bonds and other fixed-income securities. 
                       Hedging strategies, such as using options or short selling, can also help protect portfolios from downside risks. 
                       Maintaining liquidity to capitalize on future opportunities when the market recovers is also a prudent strategy."""

        plotly_jinja_data = {
            "fig": plot.to_html(full_html=False),
            "homeurl": reverse("home"),
            "marketurl": reverse("sentiment"),
            "contacturl": reverse("contact"),
            "predectionurl": reverse("predictions"),
            "indexurl": reverse("index"),
            "img_url": "{% static 'stockmarketpred/images/logo2.png' %}",
            "static_load": "{% load static %}",
            "heading1": heading1,
            "text1": text1,
            "text2": text2,
        }

        with open(output_file_path, "w", encoding="utf-8") as output_file:
            with open(input_file_path, "r", encoding="utf-8") as input_file:
                template = Template(input_file.read())
                output_file.write(template.render(plotly_jinja_data))

        return render(
            request,
            "stockmarketpred/market.html",
            {},
        )


def contact(request):
    if "u_id" not in request.session:
        return redirect("signin")
    else:
        if request.method == "GET":
            form = FeedbackForm(request.GET)
            email = request.GET.get("email")
            name = request.GET.get("name")
            phone = request.GET.get("phone")
            message = request.GET.get("message")

            print(email, name, phone, message)
            try:
                Feedback(name=name, email=email, phone=phone, message=message).save()
            except IntegrityError:
                return render(request, "stockmarketpred/contact.html", {"form": form})
            else:
                return render(request, "stockmarketpred/contact.html", {"form": form})
        else:
            form = FeedbackForm()
            print("ByPassing Data")
            return render(request, "stockmarketpred/contact.html", {"form": form})


def index(request):
    try:
        del request.session["u_id"]
    except KeyError:
        return render(request, "stockmarketpred/index.html", {})
    else:
        return render(request, "stockmarketpred/index.html", {})
