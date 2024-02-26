# import os
redirectpath = {
    "https://www.produceshop.fr/": "websites/produceshop.py",
    "https://www.vidaxl.fr/": "websites/vidaxl.py",
    "https://www.menzzo.fr/": "websites/menzzo.py",
    "https://www.premiumxl.fr/": "websites/premiumxl.py",
    "https://www.baita-home.com/": "websites/baita-home.py",
    "https://www.aosom.fr/": "websites/aosom.py",
    "https://www.roseoubleu.fr/": "websites/roseoubleu.py",
    "https://www.furnica.fr/": "websites/furnica.py",
    "https://www.oviala.com/": "websites/oviala.py",
    "https://www.habitatetjardin.com/": "websites/habitatetjardin.py",
    "https://www.kare-click.fr/": "websites/kare-click.py",
    "https://www.miliboo.com/": "websites/miliboo.py",
    "https://www.tectake.fr/": "websites/tectake.py",
    "https://www.mobilier1.fr/": "websites/mobilier1.py",
    "https://www.idmarket.com/": "websites/idmarket.py",
    "https://www.sweeek.fr/": "websites/sweeek.py",
    "https://www.atmosphera.com/": "websites/atmosphera.py",
    "https://www.beliani.fr/": "websites/beliani.py",
    "https://www.dusine.fr/": "websites/dusine.py",
    "https://www.toilinux.com/": "websites/toilinux.py",
    "https://www.concept-usine.com/": "websites/concept-usine.py",
    "https://www.pricefactory.fr/": "websites/pricefactory.py",
    "https://www.woltu.eu/": "websites/woltu.py",
    "https://www.prixton.fr/": "websites/prixton.py",
    "https://www.gorillasports.fr/": "websites/gorillasports.py",
    "https://www.1001jouets.fr/": "websites/1001jouets.py",
    "https://www.ecdgermany.de/": "websites/ecdgermany.py",
    "https://www.keter.com/": "websites/keter.py",
    "https://www.ok-living.fr/": "websites/ok-living.py",
    "https://www.at4.com/": "websites/at4.py",
    "https://www.habitium.fr/": "websites/habitium.py",
    "https://www.calicosy.com/": "websites/calicosy.py",
    "https://www.k-sport-de.de/": "websites/k-sport-de.py",
    "https://www.mobilier-deco.com/": "websites/mobilier-deco.py",
    "https://www.vente-unique.com/": "websites/vente-unique.py",
    "https://www.chaisebureau365.fr/": "websites/chaisebureau365.py",
    "https://www.temahome.com/": "websites/temahome.py",
    "https://www.5five.com/": "websites/5five.py",
    "https://www.beauxmeublespaschers.com/": "websites/beauxmeublespaschers.py",
    "https://www.natureetdecouvertes.com/": "websites/natureetdecouvertes.py",
    "https://www.songmics.fr/": "websites/songmics.py",
    "https://www.weber-industries.com/": "websites/weber-industries.py",
    "https://www.ibbedesign.fr/": "websites/ibbedesign.py",
    "https://www.caesaroo.fr/": "websites/caesaroo.py",
    "https://www.carefitness.com/": "websites/carefitness.py",
    "https://www.costway.fr/": "websites/costway.py",
    "https://www.equipementpro.fr/": "websites/equipementpro.py",
    "https://www.jardindeco.com/": "websites/jardindeco.py",
    "https://www.pegane.com/": "websites/pegane.py",
    "https://www.rendezvousdeco.com/": "websites/rendezvousdeco.py",
    "https://www.rueducommerce.fr/": "websites/rueducommerce.py",
    "https://www.vidaxl.it/": "websites/vidaxl-it.py",
    "https://www.wetsuitoutlet.fr/": "websites/wetsuitoutlet.py",
    "https://www.teamson.fr/": "websites/teamson.py",
    "https://www.vivol.fr/": "websites/vivol.py",
    "https://www.ac-deco.com/": "websites/ac-deco.py",
    "https://www.acces-design.com/": "websites/acces-design.py",
    "https://www.befara.fr/": "websites/befara.py",
    "https://www.but.fr/": "websites/but.py",
    "https://www.cadomus.com/": "websites/cadomus.py",
    "https://www.cncest.fr/": "websites/cncest.py",
    "https://www.decoratie.fr/": "websites/decoratie.py",
    "https://www.e.leclerc/": "websites/e.leclerc.py",
    "https://www.gpasplus.com/": "websites/gpasplus.py",
    "https://www.ledepot-bailleul.fr/": "websites/ledepot-bailleul.py",
    "https://www.lilifolies-airsoft.com/": "websites/lilifolies-airsoft.py",
    "https://www.ma-trading.eu/": "websites/ma-trading.py",
    "https://www.maisonetloisirs.leclerc/": "websites/maisonetloisirs.leclerc.py",
    "https://www.meubletmoi.com/": "websites/meubletmoi.py",
    "https://www.mon-abri-de-jardin.com/": "websites/mon-abri-de-jardin.py",
    "https://www.muziker.fr/": "websites/muziker.py",
}
# def create_scraper_files(redirectpath):
#     # Ensure the 'websites' directory exists
#     os.makedirs('websites', exist_ok=True)
    
#     # Function template
#     function_template = """def scraper(driver, url):
#     # Your scraping logic here
#     pass
# """

#     for path in redirectpath.values():
#         filepath = os.path.join('websites', path.split('/')[-1])
#         with open(filepath, 'w') as file:
#             file.write(function_template)
    
#     print(f"Created {len(redirectpath)} scraper files in the 'websites' directory.")

# # Execute the function with your redirectpath dictionary
# create_scraper_files(redirectpath)