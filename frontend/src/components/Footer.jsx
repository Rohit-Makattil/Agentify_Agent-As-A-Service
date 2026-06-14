function Footer() {
  const teamMembers = [
    {
      name: 'Aastha Dubey',
      instagram: 'https://www.instagram.com/aaastha.d?igsh=MWl1Z2h0ZWh4Ym13aA=',
      linkedin: 'https://www.linkedin.com/in/aastha-dubey-16a942229?utm_source=share_via&utm_content=profile&utm_medium=member_android',
      github: 'https://github.com/Aastha3105'
    },
    {
      name: 'Paridhi Gupta',
      instagram: 'https://www.instagram.com/pariiidhiiii?igsh=ZTluNnlkcHUxdjYy',
      linkedin: 'https://www.linkedin.com/in/paridhi-guptaa?utm_source=share_via&utm_content=profile&utm_medium=member_ios',
      github: 'https://github.com/paridhiiguptaa/'
    },
    {
      name: 'Shriya Jain',
      instagram: 'https://www.instagram.com/shriyaa.jainn/',
      linkedin: 'https://www.linkedin.com/in/shriyajain08/',
      github: 'https://github.com/Shriyajain08'
    },
    {
      name: 'Rohit Makattil',
      instagram: 'https://www.instagram.com/makattil.rohit?igsh=MXA3amplNW9nN3Zybg%3D%3D&utm_source=qr',
      linkedin: 'https://www.linkedin.com/in/rohit-makattil-b553852a3?utm_source=share_via&utm_content=profile&utm_medium=member_ios',
      github: 'https://github.com/Rohit-Makattil'
    }
  ];

  return (
    <footer className="footer" id="about">
      <div className="footer-content">
        <div className="team-section">
          <h3 className="team-title">Created by</h3>
          <div className="team-members">
            {teamMembers.map((member, index) => (
              <div key={index} className="member">
                <span className="member-name">{member.name}</span>
                <div className="social-links">
                  <a href={member.instagram} target="_blank" rel="noopener noreferrer" className="social-icon">
                    <i className="fab fa-instagram"></i>
                  </a>
                  <a href={member.linkedin} target="_blank" rel="noopener noreferrer" className="social-icon">
                    <i className="fab fa-linkedin-in"></i>
                  </a>
                  <a href={member.github} target="_blank" rel="noopener noreferrer" className="social-icon">
                    <i className="fab fa-github"></i>
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div className="mentor">Mentor: Mrs. Himanshi Jiwatramani</div>
        <div className="footer-divider"></div>
        <p className="footer-copyright">&copy; 2025 Agentify. All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
