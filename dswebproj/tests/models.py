from django.db import models

THEME_CHOICE= [
    ("1", "Matemática"),
    ("2", "Ciências Humanas"),
    ("3", "Ciências da Natureza"),
    ("4", "Linguagens e códigos"),
    ("5", "Conhecimentos Gerais")
]

class Question(models.Model):
    title = models.CharField(max_length=400)
    
    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    def __str__(self):
        return self.title

class Choice(models.Model):
    text = models.CharField(max_length=200)
    #img = models.ImageField()
    isRight = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')

    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"

    def __str__(self):
        return self.text
    
class Test(models.Model):
    title = models.CharField(max_length=60)
    theme = models.CharField(max_length=2, choices=THEME_CHOICE)
    questions = models.ManyToManyField(Question)

    class Meta:
        verbose_name = "Simulado"
        verbose_name_plural = "Simulados"

    def __str__(self):
        return self.title

class TestQuestionWeight(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    weight = models.IntegerField(default=1)

    class Meta:
        verbose_name = "Peso"
        verbose_name_plural = "Pesos"