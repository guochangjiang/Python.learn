var READTHEDOCS_DATA = {
    "project": "keras-cn", 
    "theme": "readthedocs", 
    "version": "latest", 
    "source_suffix": ".md", 
    "api_host": "https://readthedocs.org", 
    "language": "en", 
    "commit": "0715533a55c44ee89a1aef6b951eb1c673206d56", 
    "docroot": "/home/docs/checkouts/readthedocs.org/user_builds/keras-cn/checkouts/latest/docs", 
    "builder": "mkdocs", 
    "page": null
}

// Old variables
var doc_version = "latest";
var doc_slug = "keras-cn";
var page_name = "None";
var html_theme = "readthedocs";

READTHEDOCS_DATA["page"] = mkdocs_page_input_path.substr(
    0, mkdocs_page_input_path.lastIndexOf(READTHEDOCS_DATA.source_suffix));
