import json
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox

class TuntudEestiInimesed:
    def __init__(self, failinimi):
        with open(failinimi, 'r', encoding='utf-8') as fail:
            self.andmed = json.load(fail)

    def isikute_arv(self):
        return len(self.andmed)

    def pikim_nimi(self):
        pikim_nimi = max(self.andmed, key=lambda inimene: len(inimene['nimi']))
        return pikim_nimi['nimi'], len(pikim_nimi['nimi'])

    def arvuta_vanus(self, synniaeg, võrdluskuupäev=None):
        if võrdluskuupäev is None:
            võrdluskuupäev = datetime.now()
        synniaeg = datetime.strptime(synniaeg, '%Y-%m-%d')
        vanus = võrdluskuupäev.year - synniaeg.year - (
                (võrdluskuupäev.month, võrdluskuupäev.day) < (synniaeg.month, synniaeg.day))
        return vanus

    def vanim_inimene(self, elus=True):
        täna = datetime.now()
        inimesed = [inimene for inimene in self.andmed if (inimene['surnud'] == '0000-00-00') == elus]
        vanim_inimene = min(inimesed, key=lambda inimene: datetime.strptime(inimene['sundinud'], '%Y-%m-%d'))
        vanus = self.arvuta_vanus(vanim_inimene['sundinud'], täna)
        if not elus:
            surma_date = vanim_inimene['surnud']
            return vanim_inimene['nimi'], vanus, vanim_inimene['sundinud'], surma_date
        return vanim_inimene['nimi'], vanus, vanim_inimene['sundinud']

    def ametite_arv(self, amet):
        return len([inimene for inimene in self.andmed if inimene['amet'] == amet])

    def sündinud_aastal(self, aasta):
        return len([inimene for inimene in self.andmed if inimene['sundinud'].startswith(str(aasta))])

    def unikaalsete_elukutsete_arv(self):
        elukutsed = {inimene['amet'] for inimene in self.andmed}
        return len(elukutsed)

    def rohkem_kui_kaks_nime(self, minimaalselt_nimesid=3):
        return len([inimene for inimene in self.andmed if len(inimene['nimi'].split(" ")) >= minimaalselt_nimesid])

    def sama_synni_surmapäev(self):
        count = 0
        for inimene in self.andmed:
            if inimene['surnud'] != '0000-00-00':
                synniaeg = datetime.strptime(inimene['sundinud'], '%Y-%m-%d')
                surmaaeg = datetime.strptime(inimene['surnud'], '%Y-%m-%d')
                if synniaeg.month == surmaaeg.month and synniaeg.day == surmaaeg.day and synniaeg.year != surmaaeg.year:
                    count += 1
        return count

    def elavad_ja_surnud(self):
        elavate_arv = len([inimene for inimene in self.andmed if inimene['surnud'] == '0000-00-00'])
        surnute_arv = len(self.andmed) - elavate_arv
        return elavate_arv, surnute_arv

    def kauem_elanud_surnud_inimene(self):
        surnud_inimesed = [inimene for inimene in self.andmed if inimene['surnud'] != '0000-00-00']
        kauem_elanud_surnud = max(surnud_inimesed, key=lambda inimene: self.arvuta_vanus(inimene['sundinud'], datetime.strptime(inimene['surnud'], '%Y-%m-%d')))
        return kauem_elanud_surnud['nimi']

class TuntudEestiInimesedApp:
    def __init__(self, root, failitee):
        self.root = root
        self.root.title("Tuntud Eesti Inimesed")
        self.inimesed = TuntudEestiInimesed(failitee)

        self.create_widgets()
        self.update_info()

    def create_widgets(self):
        self.info_frame = ttk.Frame(self.root, padding="10")
        self.info_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

        self.isikute_arv_label = ttk.Label(self.info_frame, text="Isikute arv kokku:")
        self.isikute_arv_label.grid(row=0, column=0, sticky=tk.W)
        self.isikute_arv_value = ttk.Label(self.info_frame, text="")
        self.isikute_arv_value.grid(row=0, column=1, sticky=tk.W)

        self.pikim_nimi_label = ttk.Label(self.info_frame, text="Kõige pikem nimi ja tähemärkide arv:")
        self.pikim_nimi_label.grid(row=1, column=0, sticky=tk.W)
        self.pikim_nimi_value = ttk.Label(self.info_frame, text="")
        self.pikim_nimi_value.grid(row=1, column=1, sticky=tk.W)

        self.vanim_elav_label = ttk.Label(self.info_frame, text="Kõige vanem elav inimene:")
        self.vanim_elav_label.grid(row=2, column=0, sticky=tk.W)
        self.vanim_elav_value = ttk.Label(self.info_frame, text="")
        self.vanim_elav_value.grid(row=2, column=1, sticky=tk.W)

        self.vanim_surnud_label = ttk.Label(self.info_frame, text="Kõige vanem surnud inimene:")
        self.vanim_surnud_label.grid(row=3, column=0, sticky=tk.W)
        self.vanim_surnud_value = ttk.Label(self.info_frame, text="")
        self.vanim_surnud_value.grid(row=3, column=1, sticky=tk.W)

        self.naitlejate_arv_label = ttk.Label(self.info_frame, text="Näitlejate koguarv:")
        self.naitlejate_arv_label.grid(row=4, column=0, sticky=tk.W)
        self.naitlejate_arv_value = ttk.Label(self.info_frame, text="")
        self.naitlejate_arv_value.grid(row=4, column=1, sticky=tk.W)

        self.sundinud_1997_label = ttk.Label(self.info_frame, text="Sündinud 1997 aastal:")
        self.sundinud_1997_label.grid(row=5, column=0, sticky=tk.W)
        self.sundinud_1997_value = ttk.Label(self.info_frame, text="")
        self.sundinud_1997_value.grid(row=5, column=1, sticky=tk.W)

        self.elukutsed_label = ttk.Label(self.info_frame, text="Erinevaid elukutseid:")
        self.elukutsed_label.grid(row=6, column=0, sticky=tk.W)
        self.elukutsed_value = ttk.Label(self.info_frame, text="")
        self.elukutsed_value.grid(row=6, column=1, sticky=tk.W)

        self.rohkem_kui_kaks_nime_label = ttk.Label(self.info_frame, text="Nimi sisaldab rohkem kui kaks nime:")
        self.rohkem_kui_kaks_nime_label.grid(row=7, column=0, sticky=tk.W)
        self.rohkem_kui_kaks_nime_value = ttk.Label(self.info_frame, text="")
        self.rohkem_kui_kaks_nime_value.grid(row=7, column=1, sticky=tk.W)

        self.sama_synni_surmapäev_label = ttk.Label(self.info_frame, text="Sünniaeg ja surmaaeg on sama v.a. aasta:")
        self.sama_synni_surmapäev_label.grid(row=8, column=0, sticky=tk.W)
        self.sama_synni_surmapäev_value = ttk.Label(self.info_frame, text="")
        self.sama_synni_surmapäev_value.grid(row=8, column=1, sticky=tk.W)

        self.elavad_surnud_label = ttk.Label(self.info_frame, text="Elavaid ja surnud isikud:")
        self.elavad_surnud_label.grid(row=9, column=0, sticky=tk.W)
        self.elavad_surnud_value = ttk.Label(self.info_frame, text="")
        self.elavad_surnud_value.grid(row=9, column=1, sticky=tk.W)

    def update_info(self):
        self.isikute_arv_value.config(text=self.inimesed.isikute_arv())
        nimi, pikkus = self.inimesed.pikim_nimi()
        self.pikim_nimi_value.config(text=f"{nimi}, {pikkus}")

        nimi, vanus, synniaeg = self.inimesed.vanim_inimene(True)
        synniaeg_formatted = datetime.strptime(synniaeg, '%Y-%m-%d').strftime('%d.%m.%Y')
        self.vanim_elav_value.config(text=f"{nimi}, {vanus} (sündinud: {synniaeg_formatted})")

        nimi, vanus, synniaeg, surmaaeg = self.inimesed.vanim_inimene(False)
        synniaeg_formatted = datetime.strptime(synniaeg, '%Y-%m-%d').strftime('%d.%m.%Y')
        surmaaeg_formatted = datetime.strptime(surmaaeg, '%Y-%m-%d').strftime('%d.%m.%Y')
        self.vanim_surnud_value.config(
            text=f"{nimi}, {vanus} (sündinud: {synniaeg_formatted} - surnud: {surmaaeg_formatted})")

        self.naitlejate_arv_value.config(text=self.inimesed.ametite_arv('näitleja'))
        self.sundinud_1997_value.config(text=self.inimesed.sündinud_aastal(1997))
        self.elukutsed_value.config(text=self.inimesed.unikaalsete_elukutsete_arv())
        self.rohkem_kui_kaks_nime_value.config(text=self.inimesed.rohkem_kui_kaks_nime())
        self.sama_synni_surmapäev_value.config(text=self.inimesed.sama_synni_surmapäev())

        elavate_arv, surnute_arv = self.inimesed.elavad_ja_surnud()
        self.elavad_surnud_value.config(text=f"Elavaid: {elavate_arv}, Surnud: {surnute_arv}")

        kauem_elanud_surnud = self.inimesed.kauem_elanud_surnud_inimene()
        self.kauem_elanud_surnud_label = ttk.Label(self.info_frame, text="Kõige kauem elanud surnud inimene:")
        self.kauem_elanud_surnud_label.grid(row=10, column=0, sticky=tk.W)
        self.kauem_elanud_surnud_value = ttk.Label(self.info_frame, text=kauem_elanud_surnud)
        self.kauem_elanud_surnud_value.grid(row=10, column=1, sticky=tk.W)

if __name__ == "__main__":
    root = tk.Tk()
    failitee = '2018-09-18_tuntud_eesti.json'  # asenda see failinimi korrektse teega
    app = TuntudEestiInimesedApp(root, failitee)
    root.mainloop()

