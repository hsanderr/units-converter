import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk
from os.path import abspath, dirname, join


class TheApp:
    '''The Application Class.'''

    def __init__(self):
        # Build GUI
        self.builder = Gtk.Builder()
        self.builder.add_from_file('combo_ex.glade')

        # Get objects
        self.window = self.builder.get_object('window')
        self.window.set_title('Conversor de unidades')

        # Cria uma array de duas colunas, a primeira para ser uma espécie de
        # identificador, ID, e a outra, o texto mostrado. Poderia ser uma
        # coluna int e outra string, caso os Ids fossem numéricos.
        self.quantities_list = Gtk.ListStore(int, str)
        self.volume_units_list = Gtk.ListStore(int, str)
        self.temperature_units_list = Gtk.ListStore(int, str)

        # Initialize interface
        quantities = [
            [1, 'Volume'],
            [2, 'Temperatura']]

        for qty in quantities:
            self.quantities_list.append(qty)

        volume_units = [
            [1, 'milímetros cúbicos (mm³)'],
            [2, 'centímetros cúbicos (cm³)'],
            [3, 'litros (L)']]

        temperature_units = [
            [1, 'Celsius'],
            [2, 'Farenheint'],
            [3, 'Kelvin']
        ]

        for unity in volume_units:
            self.volume_units_list.append(unity)

        for unity in temperature_units:
            self.temperature_units_list.append(unity)

        # Associando a array (ListStore) ao ComboBox
        self.combo1 = self.builder.get_object('combo1')
        self.combo1.set_model(self.quantities_list)

        self.unity_from = self.builder.get_object('combo_from')
        self.unity_to = self.builder.get_object('combo_to')
        self.unity_from.set_model(self.volume_units_list)
        self.unity_to.set_model(self.volume_units_list)

        # É necessário adicionar um renbderizador de texto ao ComboBox
        renderer_text = Gtk.CellRendererText()
        self.combo1.pack_start(renderer_text, True)
        self.unity_from.pack_start(renderer_text, True)
        self.unity_to.pack_start(renderer_text, True)

        # Escolher qual coluna mostrar:
        self.combo1.add_attribute(renderer_text, "text", 1)
        self.unity_from.add_attribute(renderer_text, "text", 1)
        self.unity_to.add_attribute(renderer_text, "text", 1)

        # Opção ativa default
        self.combo1.set_active(0)

        # Connect signals
        self.builder.connect_signals(self)

        # Everything is ready
        self.window.show()

    def on_window_destroy(self, widget):
        '''Classical window close button.'''
        Gtk.main_quit()

    # def on_button_clicked(self, button):
    #     '''Do something...'''
    #     model = self.combo.get_model()
    #     active = self.combo.get_active()
    #     if (not (active < 0)):
    #         print("Opção selecionada: {} ({})".format(model[active][0], model[active][1]))
    #     else:
    #         print("Error")

    def on_combo1_changed(self, widget):
        '''Verify which option is selected'''
        model = widget.get_model()
        active = widget.get_active()
        option = model[active][1]
        print('Opção selecionada: {}'.format(option))
        if active == 0:
            self.unity_from.set_model(self.volume_units_list)
        if active == 1:
            self.unity_from.set_model(self.temperature_units_list)

        # if active >= 0:
        #     code = model[active][0]
        #     print('Opção selecionada: {}'.format(code))
        # else:
        #     print('Sem opção.')


if __name__ == '__main__':
    try:
        gui = TheApp()
        Gtk.main()
    except KeyboardInterrupt:
        pass
