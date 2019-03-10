FROM ibmcom/websphere-traditional:9.0.0.9-profile
COPY app.ear /work/config/app.ear
COPY SSMAdmin2.ear /work/config/SSMAdmin2.ear
COPY SSMServer2.ear /work/config/SSMServer2.ear
COPY install_app.py /work/config/install_app.py
COPY postgresql-9.4-1206-jdbc42.jar /work/config/postgresql-9.4-1206-jdbc42.jar
COPY --chown=was:was ibmcloud.cer /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/etc/ibmcloud.cer
COPY was-config.props /work/config/was-config.props
COPY --chown=was:was ssl.client.props /opt/IBM/WebSphere/AppServer/profiles/AppSrv01/properties/ssl.client.props
RUN /work/configure.sh
EXPOSE 9443 9043 
