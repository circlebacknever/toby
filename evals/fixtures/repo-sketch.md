# Repo sketch: teamdesk

This file describes a small Django app for the feature-dev design eval. It lists the files a planner needs and quotes the code in them. Treat every path and line number as real.

## Layout

```
app/
  orgs/models.py          Org, Member
  billing/plans.py        plan names and prices
  billing/page.py         the billing page view
  invites/views.py        POST /invites and the invite form
  invites/service.py      InviteService
  invites/repository.py   InviteRepository
  api/serializers.py      OrgSerializer for the public API
  api/views.py            POST /api/orgs/<id>/invites
tests/
  test_invites.py
  test_billing_page.py
```

## app/orgs/models.py

```python
class Org(models.Model):                      # line 4
    name = models.CharField(max_length=200)
    plan = models.CharField(max_length=20)    # "free", "team", or "enterprise"

class Member(models.Model):                   # line 9
    org = models.ForeignKey(Org, on_delete=models.CASCADE, related_name="members")
    email = models.EmailField()
    role = models.CharField(max_length=20)    # "admin" or "member"
```

## app/billing/plans.py

```python
PLAN_NAMES = ["free", "team", "enterprise"]   # line 1

def monthly_price(plan):                      # line 3
    if plan == "free":
        return 0
    elif plan == "team":
        return 8
    elif plan == "enterprise":
        return 20
```

## app/billing/page.py

```python
def billing_page(request):                    # line 6
    org = request.org
    if org.plan == "free":
        features = ["3 projects"]
    elif org.plan == "team":
        features = ["unlimited projects", "SSO"]
    elif org.plan == "enterprise":
        features = ["unlimited projects", "SSO", "audit log"]
    return render(request, "billing/page.html", {"org": org, "features": features})
```

## app/api/serializers.py

```python
class OrgSerializer(serializers.ModelSerializer):   # line 3
    features = serializers.SerializerMethodField()

    def get_features(self, org):                    # line 6
        if org.plan == "free":
            return {"sso": False, "audit_log": False}
        elif org.plan == "team":
            return {"sso": True, "audit_log": False}
        elif org.plan == "enterprise":
            return {"sso": True, "audit_log": True}
```

## app/invites/service.py

```python
class InviteService:                                  # line 1
    def __init__(self, repo):
        self.repo = repo

    def create(self, org, email, invited_by):         # line 5
        return self.repo.create(org, email, invited_by)

    def list_pending(self, org):                      # line 8
        return self.repo.list_pending(org)
```

## app/invites/repository.py

```python
class InviteRepository:                               # line 1
    def create(self, org, email, invited_by):
        return Invite.objects.create(org=org, email=email, invited_by=invited_by)

    def list_pending(self, org):
        return Invite.objects.filter(org=org, accepted_at__isnull=True)
```

## app/invites/views.py

```python
def create_invite(request):                           # line 10
    form = InviteForm(request.POST)
    if not form.is_valid():
        return render(request, "invites/form.html", {"form": form}, status=400)
    service = InviteService(InviteRepository())
    service.create(request.org, form.cleaned_data["email"], request.user)
    return redirect("members")
```

## app/api/views.py

```python
class OrgInvitesView(APIView):                        # line 14
    def post(self, request, org_id):
        org = get_object_or_404(Org, id=org_id, members__email=request.user.email)
        service = InviteService(InviteRepository())
        invite = service.create(org, request.data["email"], request.user)
        return Response({"id": invite.id}, status=201)
```

## Tests

`tests/test_invites.py` covers `create_invite` with a valid and an invalid email. `tests/test_billing_page.py` checks that the page renders for each of the three plans. No test covers `OrgInvitesView`.

## Facts from the product team

- Seat caps by plan: free 3, team 50, enterprise unlimited.
- A pending invite counts as a seat, because the product team wants the cap to hold when many invites are accepted at once.
- The billing page is visible to admins only.
