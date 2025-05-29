from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext as _


class FormView:
    def get(self, request):
        values = self.value.objects.all()
        return render(request, self.template, context={"values": values})


class DeleteView:
    def get(self, request, *args, **kwargs):
        value_id = kwargs.get("pk")
        value = self.value.objects.get(id=value_id)
        return render(
            request,
            self.template,
            {"value": value, "value_id": value_id},
        )


class EditView:
    def post(self, request, *args, **kwargs):
        obj = self.value.objects.get(pk=kwargs.get("pk"))
        form = self.form(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, _(self.text))
            return redirect(f"{self.path}:list")
        return render(request, self.template, {"form": form})
