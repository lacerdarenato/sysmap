from anticaptchaofficial.hcaptchaproxyless import *
from environs import Env

env = Env()
env.read_env()

def solve_captcha(page):
  time.sleep(1000)
  site_url= page.locator('.h-captcha').get_attribute('data-sitekey')
  solver = hCaptchaProxyless()
  solver.set_verbose(1)
  solver.set_key(env.API_SOLVE_CAPTCHA_KEY)
  solver.set_website_url(site_url)

  solver.set_soft_id(0)

  g_response = solver.solve_and_return_solution()
  if g_response:
    return g_response
  
def wait_seconds_to_user_click(seconds):
    print('**** por favor clique no captcha ****')
    time.sleep(seconds)