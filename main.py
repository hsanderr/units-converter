import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from os.path import abspath, dirname, join

class App:

    def __init__(self):
        # GUI
        self.builder = Gtk.Builder()
        self.builder.add_from_file('converter.glade')

        # Get window object and set title
        self.window = self.builder.get_object('window')
        self.window.set_title('Conversor de unidades')

        # Quantities and units arrays
        self.quantities_list = Gtk.ListStore(int, str)
        self.volume_units_list = Gtk.ListStore(int, str)
        self.temperature_units_list = Gtk.ListStore(int, str)

        # Quantities
        quantities = [
            [1, 'Volume'],
            [2, 'Temperatura']]

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

        for unit in volume_units:
            self.volume_units_list.append(unit)

        for unit in temperature_units:
            self.temperature_units_list.append(unit)

        # Configuring comboboxes options
        self.combo1 = self.builder.get_object('combo1')
        self.combo_from = self.builder.get_object('combo_from')
        self.combo_to = self.builder.get_object('combo_to')
        self.combo1.set_model(self.quantities_list)
        self.unit_from = self.builder.get_object('combo_from')
        self.unit_to = self.builder.get_object('combo_to')
        self.unit_from.set_model(self.volume_units_list)
        self.unit_to.set_model(self.volume_units_list)

        # comboxes renderer
        renderer_text = Gtk.CellRendererText()
        self.combo1.pack_start(renderer_text, True)
        self.unit_from.pack_start(renderer_text, True)
        self.unit_to.pack_start(renderer_text, True)

        # Escolher qual coluna mostrar:
        self.combo1.add_attribute(renderer_text, "text", 1)
        self.unit_from.add_attribute(renderer_text, "text", 1)
        self.unit_to.add_attribute(renderer_text, "text", 1)

        # Default option
        self.combo1.set_active(0)
        self.combo_from.set_active(0)
        self.combo_to.set_active(0)
        self.unitFrom = 1
        self.unitTo = 1

        # Connect signals
        self.builder.connect_signals(self)

        # Show window
        self.window.show()

        self.quantity = 0 # quantity=0: volume, quantity=1: temperature

        self.input = self.builder.get_object('input')
        self.out = self.builder.get_object('output')

    def on_window_destroy(self, widget):
        '''Classical window close button.'''
        Gtk.main_quit()

    def on_combo1_changed(self, widget):
        '''Verify which option is selected'''
        model = widget.get_model()
        active = widget.get_active()
        option = model[active][1]
        self.input.set_text('')
        self.combo_from.set_active(0)
        self.combo_to.set_active(0)
        print('Opção selecionada: {}'.format(option))
        if active == 0:
            self.unit_from.set_model(self.volume_units_list)
            self.unit_to.set_model(self.volume_units_list)
            self.quantity = 0
        if active == 1:
            self.unit_from.set_model(self.temperature_units_list)
            self.unit_to.set_model(self.temperature_units_list)
            self.quantity = 1

    def on_from_changed(self, widget):
        model = widget.get_model()
        active = widget.get_active()
        option = model[active][0]
        self.input.set_text('')
        self.unitFrom = option

    def on_to_changed(self, widget):
        model = widget.get_model()
        active = widget.get_active()
        option = model[active][0]
        self.input.set_text('')
        self.unitTo = option

    def on_input_changed(self, widget):
        input = widget.get_text()
        if (input == ''):
            self.out.set_text('')
        if (input.isdigit()):
            if (self.quantity == 0):
                if (self.unitFrom == self.unitTo):
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
            if (self.quantity == 1):
                if (self.unitFrom == self.unitTo):
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
