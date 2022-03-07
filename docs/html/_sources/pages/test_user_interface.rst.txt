User Interface
=======================================================

Wrapped Text Rendering
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Text block rendering is tested manually. The main purpose of the test is that
individual lines of text should not be interrupted or shortened by the Blender
User Interface.

.. image:: ../images/test_wrapped_text.gif
    :align: center

--------------------------------------------------------------------------------

The main criteria are the following:

* The text block is displayed in full

* No lines ending or separated by dots


Developer Extras UI
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

.. image:: ../images/test_developer_extras_ui.gif
    :align: center


--------------------------------------------------------------------------------

Progress Bars
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

Testing the progress bars is done manually because their implementation is quite
complex.

.. image:: ../images/test_progress_bars.gif
    :align: center


--------------------------------------------------------------------------------

The main criteria are the following:

* After initiating the progress bar, the original User Interface status bar is stored.

* After the disappearance of the last progress of the bar, the original method of displaying the status bar is completely restored.

* The initiated progress bar is to the right of the previous one.

* For each status bar you can change its basic parameters that affect its display (title, icon, etc.).
