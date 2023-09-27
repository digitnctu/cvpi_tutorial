.. cvpi_tutorial documentation master file, created by
   sphinx-quickstart on Wed Mar  1 11:20:15 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to cvpi_tutorial's documentation!
=========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   tutorial
   case1   


.. ::

	ditaa(-E -S, scale=1.2)
    +---------------+ +---------+ +----------+
    | cBLU          | | cBLU    | | cRED     |
    | driver        | | BUS_INF | | SW       |
    |   +-----------+ |         | |          |
    |   |   DUT     +-+         +-+          |
    |   +-----------+ +---------+ +----------+
    |   |   cAAA    | | c22E    | | cPNK     |
    |   |   param   +-+ gen_pat +-+ drv_pat  |
    |   |           | |         | |          |
    |   +----+------+ +---------+ +----------+
    |        | cBLU |                         
    |   +----+------+ +----------------------+
    |   |   c2E2    | | cPNK                 |
    |   |   emd_scr +-+ scr_pat              |
    |   |           | |                      |
    +---+----+------+ +----------------------+


.. 
	graphviz::

	digraph example {
		a->b
    }

.. 
	wavedrom::

	{ "signal": [
		 { "wave":"P...........", "name":"clk",
		   "node":"............", "data":[]
		}
		,{ "wave":"22..........", "name":"data",
		   "node":"............", "data":["a1","a2"]
		}
	  ]
    }

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
