from shiny import App, render, ui
import os

species = {'maize':'Zea mays',
           'rice':'Oryza sativa',
           'arabidopsis':'Arabidopsis thaliana',
           'apple':'Malus domestica',
           'sorghum':'Sorghum bicolor',
           'grape':'Vitis vinifera',
           'mustard':'Brassica rapa',
           'soybean':'Glycine max',
           'medicago':'Medicago truncatula',
           'tobacco':'Nicotiana tabacum',
           'potato':'Solanum tuberosum',
           'brome':'Brachypodium distachyon',
           'tomato':'Solanum lycopersicum'
           }
stringent = {'moderate':'Moderate','lenient':'Lenient','stringent':'Stringent'}
#choices = {"a": "Choice A", "b": "Choice B"}
os.chdir(os.path.dirname(os.path.abspath(__file__)))
current_dir = os.getcwd()
all_files_in_folder = os.listdir(current_dir+'/Species_species_gene_tables')
def ui_card(title, *args):
    return (
        ui.div(
            {"class": "card mb-4"},
            ui.div(title, class_="card-header"),
            ui.div({"class": "card-body"}, *args),
        ),
    )

app_ui = ui.page_fluid(
    ui.h1({'style':'text-align:center;'},"EPIPHITES: Expression Proxies In Plants Help Integrate Transcribed Expression in Single-cell"),
    ui.row(ui.p("\n")),
    ui.row(ui.p("\n")),
    ui.row(ui.p("\n")),
    ui.row(
        ui.column(
            4, ui.h2({"class": "card-title m-0",'style':'text-align:center;'},'Welcome to EPIPHITES'),
            ui.h6('Background'),
            ui.p(
                """
                Integrating cross species scRNAseq data is an increasingly common challenge for plant
                biologists seeking to answer challenging questions about cell type specific innovations critical to 
                domestication, yield, and pathogen resistance traits. We developed EPIPHITES(Expression Proxies In Plants Help Integrate Transcribed Expression in Single-cell)
                to facillitate this integration integration.
                """
                ),
            ui.h6('Premise'),
            ui.p(
                """
                We use meta-analysis from prior bulk data to define co-expression proxies that can be applied in more specific, but less well-powered, specific single cell data.
                Although our proxies may not be 1-1 matches between species, they are similar enough to serve as proxies for integration in a high dimensional space
                (such as cell types) and improve the integration of cross species single-cell data.
                """
                ),

        ),
        ui.column(
            6,
            ui.img(src ="expressalog_diagram_for_shiny_trimmed.png"),
        ),
    ),
    ui.row(
     ui.h6('Use'),
     ui.p("""
     Our proxy lists can be utilized as if they were orthologs between  two species, expanding the shared gene space traditionally operated upon by 
     other integration methods. After aligning two expression datasets using our coexpression proxies, they can be integrated with any other integration method,
     such as Seurat, Scanorama, or ScANVI.
     """
          ),
    ),
    ui.div(
        {'class':'card mb-3'},
        ui.div(
            {'class':'card-body'},
            ui.h4({"class": "card-title m-0"},'Select Species'),
            ui.div(
                {'class':'card-body overflow-auto pt-3'},
                ui.layout_sidebar(
                    ui.input_select( "species_1",'Species 1', species),
                    ui.input_select("species_2",'Species 2',species),
                ),
            ),
        ),
        ui.div(
            {'class':"card-footer"},
            ui.output_text("species_txt"),
        )
        
    ),
    ui.div(
        {'class':'card mb-3'},
        ui.div(
            {'class':'card-body'},
            ui.h4({"class": "card-title m-0"},'Select Thresholding'),
            ui.div(
                {'class':'card-body overflow-auto pt-3'},
                ui.input_select("stringency",'Coexpression Conservation Threshold', stringent),
                ),
            ),
        
        ui.div(
            {'class':"card-footer"},
            ui.output_text("stringency_txt"),
            ),
        ),
        

    ui.panel_conditional(
        "input.species_1 !== input.species_2",
        ui.div(
        {"class": "card mb-4"},
        ui.div('Download', class_="card-header"),
        ui.div(
            {"class": "card-body"},
            ui.download_button("download1","Download Coexpression Proxies")
            ),
        ),
    ),
)

#    ui.output_text_verbatim("txt"),



def server(input, output, session):
    @output
    @render.text
    def species_txt():
        if input.species_1() == input.species_2():
            return "Species are the same, please select two different species"
        else:
            return f"Generate {input.species_1()} to {input.species_2()} table"
        

    @output
    @render.ui
    def images() -> ui.Tag:
        img = ui.img(src="/data/passala/git/Coexpressalog_Method_Development/shiny_for_proxy_paper/783px-Test-Logo.svg.png",)
        return img    
    

    @output
    @render.text
    def stringency_txt():
            if input.species_1() == input.species_2():
                return "Awaiting species selection" 
            else:
                 return f"Generate {input.species_1()} to {input.species_2()} table with {input.stringency()} thresholding"

    @session.download(filename = lambda:f'{input.species_1()}_{input.species_2()}_{input.stringency()}_coexpressalog_table.csv')
    def download1():
        # This is the simplest case. The implementation simply returns the path to a
        # file on disk.
        spec_1_filter = [i for i in all_files_in_folder if input.species_1() in i]
        spec_2_filter = [i for i in spec_1_filter if input.species_2() in i]
        final_file = [i for i in spec_2_filter if input.stringency() in i]
        current_file = final_file[0]
        full_location = current_dir'/Species_species_gene_tables/'+current_file
        return full_location
app = App(app_ui, server,static_assets=current_dir+'/static_assets')
