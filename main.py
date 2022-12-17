# Henrique Sander Lourenço
# 10802705

import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from os.path import abspath, dirname, join

# Create App class
class App:

    def __init__(self):

        # Connect to glade file
        self.builder = Gtk.Builder()
        self.builder.add_from_file('converter.glade')

        # Get window object and set title
        self.window = self.builder.get_object('window')
        self.window.set_title('Conversor de unidades')

        # Create quantities and units lists in Gtk
        self.quantities_list = Gtk.ListStore(int, str)
        self.volume_units_list = Gtk.ListStore(int, str)
        self.temperature_units_list = Gtk.ListStore(int, str)

        # Quantities
        quantities = [
            [1, 'Volume'],
            [2, 'Temperatura']]

        # Append quantities to Gtk list
        for qty in quantities:
            self.quantities_list.append(qty)

        # Volume units
        volume_units = [
            [1, 'milímetros cúbicos (mm³)'],
            [2, 'centímetros cúbicos (cm³)'],
            [3, 'litros (L)']]

        # Temperature units
        temperature_units = [
            [1, 'Celsius'],
            [2, 'Farenheint'],
            [3, 'Kelvin']
        ]

        # Append volume units to Gtk list
        for unit in volume_units:
            self.volume_units_list.append(unit)

        # Append temperature units to Gtk list
        for unit in temperature_units:
            self.temperature_units_list.append(unit)

        # Configure combo boxes
        self.combo_qty = self.builder.get_object('combo_qty') # Quantities combo box
        self.combo_from = self.builder.get_object('combo_from') # 'From units' combo box
        self.combo_to = self.builder.get_object('combo_to') # 'To units' combo box
        self.combo_qty.set_model(self.quantities_list) # Set quantities combo box model
        self.combo_from.set_model(self.volume_units_list) # Set 'from units' combo box model
        self.combo_to.set_model(self.volume_units_list) # Set 'to units' combo box model

        # Add combo boxes renderer
        renderer_text = Gtk.CellRendererText()
        self.combo_qty.pack_start(renderer_text, True)
        self.combo_from.pack_start(renderer_text, True)
        self.combo_to.pack_start(renderer_text, True)

        # Choose what to show on combo boxes
        self.combo_qty.add_attribute(renderer_text, "text", 1)
        self.combo_from.add_attribute(renderer_text, "text", 1)
        self.combo_to.add_attribute(renderer_text, "text", 1)

        # Default options
        self.combo_qty.set_active(0)
        self.combo_from.set_active(0)
        self.combo_to.set_active(0)
        self.unitFrom = 1 # Tell which unit the quantity is being converted from
        self.unitTo = 1 # Tell which unit the quantity is being converted to

        # Connect signals
        self.builder.connect_signals(self)

        # Show window
        self.window.show()

        self.quantity = 0 # Tell which quantity is being converted (0 is volume and 1 is temperature)

        self.input = self.builder.get_object('input')
        self.out = self.builder.get_object('output')

    # Close window button
    def on_window_destroy(self, widget):
        Gtk.main_quit()

    # Quantity being converted changed
    def on_qty_changed(self, widget):
        model = widget.get_model()
        active = widget.get_active()
        option = model[active][1] # Get which quantity is selected
        self.input.set_text('')
        # print('Opção selecionada: {}'.format(option)) # Debug only
        if active == 0: # Volume selected
            self.combo_from.set_model(self.volume_units_list)
            self.combo_to.set_model(self.volume_units_list)
            self.combo_from.set_active(0) # Clear 'from units' combo box
            self.combo_to.set_active(0) # Clear 'to units' combo box
            self.quantity = 0
        if active == 1: # Temperature selected
            self.combo_from.set_model(self.temperature_units_list)
            self.combo_to.set_model(self.temperature_units_list)
            self.combo_from.set_active(0) # Clear 'from units' combo box
            self.combo_to.set_active(0) # Clear 'to units' combo box
            self.quantity = 1

    # From unit changed
    def on_from_changed(self, widget):
        model = widget.get_model()
        active = widget.get_active()
        option = model[active][0]
        self.unitFrom = option
        input_text = self.input.get_text()
        self.input.set_text('') # So that on_input_changed is called
        self.input.set_text(input_text)

    # To unit changed
    def on_to_changed(self, widget):
        model = widget.get_model()
        active = widget.get_active()
        option = model[active][0]
        self.unitTo = option
        input_text = self.input.get_text()
        self.input.set_text('') # So that on_input_changed is called
        self.input.set_text(input_text)

    # Input changed
    def on_input_changed(self, widget):
        input = widget.get_text()
        if (input == ''): # Input is empty
            self.out.set_text('')
        if (input.isdigit()): # Input is a number
            # Volume conversion
            if (self.quantity == 0):
                if (self.unitFrom == self.unitTo): # Same units
                    self.out.set_text(input)
                if (self.unitFrom == 1 and self.unitTo == 2): # mm3 to cm3
                    self.out.set_text(str(int(input) / 1000))
                if (self.unitFrom == 1 and self.unitTo == 3): # mm3 to L
                    self.out.set_text(str(int(input) / 1000000))
                if (self.unitFrom == 2 and self.unitTo == 1): # cm3 to mm3
                    self.out.set_text(str(int(input) * 1000))
                if (self.unitFrom == 2 and self.unitTo == 3): # cm3 to L
                    self.out.set_text(str(int(input) / 1000))
                if (self.unitFrom == 3 and self.unitTo == 1): # L to mm3
                    self.out.set_text(str(int(input) * 1000000))
                if (self.unitFrom == 3 and self.unitTo == 2): # L to cm3
                    self.out.set_text(str(int(input) * 1000))
            # Temperature conversion
            if (self.quantity == 1):
                if (self.unitFrom == self.unitTo): # Same units
                    self.out.set_text(input)
                if (self.unitFrom == 1 and self.unitTo == 2): # Celsius to Farenheint
                    self.out.set_text(str(int(input) * 9 / 5 + 32))
                if (self.unitFrom == 1 and self.unitTo == 3): # Celsius to Kelvin
                    self.out.set_text(str(int(input) + 273.15))
                if (self.unitFrom == 2 and self.unitTo == 1): # Farenheint to Celsius
                    self.out.set_text(str((int(input) - 32) * 5 / 9))
                if (self.unitFrom == 2 and self.unitTo == 3): # Farenheint to Kelvin
                    self.out.set_text(str((int(input) - 32) * 5 / 9 + 273.15))
                if (self.unitFrom == 3 and self.unitTo == 1): # Kelvin to Celsius
                    self.out.set_text(str(int(input) - 273.15))
                if (self.unitFrom == 3 and self.unitTo == 2): # Kelvin to Farenheint
                    self.out.set_text(str((int(input) - 273.15) * 9 / 5 + 32))
        

if __name__ == '__main__':
    try:
        gui = App()
        Gtk.main()
    except KeyboardInterrupt:
        pass
