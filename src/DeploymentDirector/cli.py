import click
import yaml

from .utils import eprint

from DeploymentDirector import DeploymentDirector

@click.command()
@click.option('--ci-name', help='Name of the CI product deployment director is running under', envvar='CI_NAME')
@click.option('--dry-run', '-n', help='Do not actually execute any actions, just print them out')
@click.option('--verbose', '-v', count=True)
@click.argument('rules_file', type=click.File('r'))
def main(rules_file, **options):
  rules = yaml.load(rules_file)
  dd = DeploymentDirector(rules, options=options)
  actions_ok = dd.run_deployment()
  if len(dd.actions) > 0:
    click.echo('\n')
    click.secho('===== ACTION RESULT SUMMARY ======', fg='cyan', bold=True)
    for (name,action) in dd.actions.iteritems():
      color = None
      text = 'not run'
      if action.succeeded is not None:
        color = 'green' if action.succeeded else 'red'
        text = 'SUCCESS' if action.succeeded else 'FAIL'
      click.secho('  - %s: %s' % (name, text), fg=color)
  if actions_ok:
    click.secho('\n===== SUCCESS =====', fg='green', bold=True)
    return 0
  else:
    click.secho('\n+++++ SOME ERRORS ENCOUNTERED +++++', fg='red', bold=True)
    raise SystemExit(1)
