
from django.core.management.base import BaseCommand

from ...models import StatsModel

class Command(BaseCommand):
    help = "My shiny new management command."

    def stats_model_subclasses(self):
        def collect(basecls):
            collected = set()
            for subcls in basecls.__subclasses__():
                collected.add(subcls)
                collected.update(collect(subcls))
            return collected
        return tuple(collect(StatsModel))


    def handle(self, *args, **options):
        for cls in self.stats_model_subclasses():
            import ipdb; ipdb.set_trace()
