import dash_bootstrap_components as dbc


def Navbar():
     navbar = dbc.NavbarSimple(
           children=[
              dbc.NavItem(dbc.NavLink("Pipe-Dream", href="/Pipe-dreams")),
              dbc.NavItem(dbc.NavLink("Scattergories", href="/Scattergories")),
              dbc.NavItem(dbc.NavLink("Interact", href="/Interact")),
              dbc.DropdownMenu(
                 nav=True,
                 in_navbar=True,
                 label="Menu",
                 children=[
                    dbc.DropdownMenuItem("Entry 1"),
                    dbc.DropdownMenuItem("Entry 2"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Entry 3"),
                          ],
                      ),
                    ],
          brand="Home",
          brand_href="/home",
          sticky="top",
        )
     return navbar
