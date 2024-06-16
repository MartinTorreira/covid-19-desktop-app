#!/usr/bin/env python3
import sys
import textwrap
from collections import namedtuple
import time

import gi
gi.require_version('Atspi', '2.0')
from gi.repository import Atspi
import ipm.e2e


def show(text):
	print(textwrap.dedent(text))

def show_passed():
	print('\033[92m', "    Passed", '\033[0m')

def show_not_passed(e):
	print('\033[91m', "    Not passsed", '\033[0m')
	print(textwrap.indent(str(e), "    "))


Ctx = namedtuple("Ctx", "path process app")

def given_app_launched(ctx):
	process, app = ipm.e2e.run(ctx.path)
	assert app is not None
	return Ctx(path= ctx.path, process= process, app= app)

def then_i_see_label(ctx, name):
    gen = (node for _path, node in ipm.e2e.tree_walk(ctx.app) if node.get_role_name() == 'label' and node.get_text(0, -1).startswith(name))
    label = next(gen, None)
    assert label and label.get_text(0, -1) == name, label.get_text(0, -1)
    return ctx
    
def then_i_see_entry(ctx, name):
	gen = (node for _path, node in ipm.e2e.tree_walk(ctx.app) if node.get_role_name() == 'entry')
	entry = next(gen, None)
	return ctx
	
def then_i_see_button(ctx, name):
    gen = (node for _path, node in ipm.e2e.tree_walk(ctx.app) if node.get_role_name() == 'push button' and node.get_name() == name)
    button = next(gen, None)
    assert button and button.get_name() == name, button.get_name()
    return ctx
    
def when_i_press_button(ctx, name):
    gen = (node for _path, node in ipm.e2e.tree_walk(ctx.app) if node.get_role_name() == 'push button' and node.get_name() == name)
    button = next(gen, None)
    do, shows = ipm.e2e.perform_on(ctx.app)
    do('click', role= 'push button', name= name)
    return ctx
    

if __name__== "__main__":
	sut_path = sys.argv[1]
	initial_ctx = Ctx(path= sut_path, process= None, app= None)

	show("""
	GIVEN he lanzado la aplicación
	THEN veo la label de Nombre y apellidos.
	THEN veo el boton de Buscar
	""")
	ctx = initial_ctx
	try:
		ctx = given_app_launched(ctx)
		time.sleep(1)
		ctx = then_i_see_label(ctx, "Nombre y apellidos")
		time.sleep(1)
		ctx = then_i_see_entry(ctx, " ")
		time.sleep(1)
		ctx = then_i_see_button(ctx, "Buscar")
		time.sleep(1)
		show_passed()
	except Exception as e:
		show_not_passed(e)

	ctx.process and ctx.process.kill()
	
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
