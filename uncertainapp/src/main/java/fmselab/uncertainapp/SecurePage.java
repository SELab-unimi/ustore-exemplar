package fmselab.uncertainapp;

import com.vaadin.navigator.View;
import com.vaadin.navigator.ViewChangeListener.ViewChangeEvent;
import com.vaadin.server.Page;
import com.vaadin.server.VaadinSession;
import com.vaadin.ui.Button;
import com.vaadin.ui.Button.ClickEvent;
import com.vaadin.ui.Button.ClickListener;
import com.vaadin.ui.Label;
import com.vaadin.ui.VerticalLayout;

public class SecurePage extends VerticalLayout implements View {
	private static final long serialVersionUID = 1L;
	private Label secure;
	private Button otherSecure;
	private Button logout;
	public static final String NAME = "Secure";

	public SecurePage() {
		
		otherSecure = new Button("OtherSecure");
		otherSecure.addClickListener(new ClickListener() {
			private static final long serialVersionUID = 1L;

			@Override
			public void buttonClick(ClickEvent event) {
				Page.getCurrent().setUriFragment("!"+OtherSecurePage.NAME);
			}
		});
		
		logout = new Button("Logout");
		logout.addClickListener(new ClickListener() {
			private static final long serialVersionUID = 1L;

			@Override
			public void buttonClick(ClickEvent event) {
				getUI().getNavigator().removeView(SecurePage.NAME);
				getUI().getNavigator().removeView(OtherSecurePage.NAME);
				VaadinSession.getCurrent().setAttribute("user", null);
				Page.getCurrent().setUriFragment("");
			}
		});
		
		secure = new Label("secure");

		addComponent(secure);
		addComponent(otherSecure);
		addComponent(logout);		
	}

	@Override
	public void enter(ViewChangeEvent event) {

	}

}
